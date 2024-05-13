# asr.py

from whisper_streaming.whisper_online import *
from configuration import SRC_LAN

# Load Whisper ASR model
asr = WhisperTimestampedASR(SRC_LAN, 'small')

# Create online ASR processor
online = OnlineASRProcessor(asr)

# Callback function to capture audio from the microphone and write to file
def process_audio_chunk(indata, status, wave_file):
    if status:
        print(status)
    audio_data = indata[:, 0]  # Assuming mono audio, take the first channel
    online.insert_audio_chunk(audio_data)
    output = online.process_iter()
    if output:
        print(output)
    wave_file.write(indata)  # Write raw audio data to the file

def finalize_asr(wave_file):
    wave_file.close()
    final_output = online.finish()
    print(final_output)
    online.init()  # Reinitialize if needed for further use
