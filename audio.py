# audio.py

import sounddevice as sd
import soundfile as sf
from configuration import SAMPLERATE, CHANNELS, FILENAME
from asr import process_audio_chunk, finalize_asr

def record_and_process_audio(filename=FILENAME, duration=10):
    """Records audio from the microphone, processes it through ASR, and saves it to a file."""
    print("Recording and processing...")

    # Setup wave file for output
    wave_file = sf.SoundFile(filename, mode='w', samplerate=SAMPLERATE, channels=CHANNELS, format='WAV', subtype='PCM_16')

    # Define the callback to handle incoming data
    def callback(indata, frames, time, status):
        if status:
            print(status)
        process_audio_chunk(indata, status, wave_file)

    # Setup the audio input stream
    with sd.InputStream(samplerate=SAMPLERATE, channels=CHANNELS, dtype='float32', callback=callback):
        sd.sleep(duration * 1000)  # active recording and processing for 'duration' seconds

    # Finalize ASR and file writing
    finalize_asr(wave_file)

    print("Recording and ASR processing complete. Output saved to:", filename)

