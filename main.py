import sounddevice as sd
import numpy as np
import queue
import threading
import tempfile
from faster_whisper import WhisperModel
from scipy.io.wavfile import write

model_size = 'small'
model = WhisperModel(model_size, device='cpu', compute_type='int8')

q = queue.Queue()
sample_rate = 16000  # Ensure the sample rate matches the model's expected input

def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(indata.copy())

def process_audio():
    while True:
        audio_buffer = q.get()
        if audio_buffer is None:
            break
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=True) as tmpfile:
            write(tmpfile.name, sample_rate, audio_buffer)
            segments, _ = model.transcribe(tmpfile.name, beam_size=5)
            for segment in segments:
                print('[%.2fs -> %.2fs] %s' % (segment.start, segment.end, segment.text))

# Start the audio processing thread
threading.Thread(target=process_audio, daemon=True).start()

# Start the audio stream
with sd.InputStream(samplerate=sample_rate, channels=1, callback=audio_callback):
    print("Recording... Press Ctrl+C to stop.")
    try:
        while True:
            sd.sleep(1000)
    except KeyboardInterrupt:
        print("Stopped recording.")
        q.put(None)  # Stop the audio processing thread
