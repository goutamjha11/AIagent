import os

import sounddevice as sd
from scipy.io.wavfile import write
from dotenv import load_dotenv
import openai

load_dotenv()
OPENAI_API_KEY= os.getenv("OPENAI_API_KEY")

# Set your OpenAI API key


def speech_to_text(audio_file):
    """
    Convert speech to text using OpenAI's Whisper API.

    Parameters:
        audio_file (str): The path to the audio file (WAV, MP3, etc.).

    Returns:
        str: Transcribed text.
    """
    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    with open(audio_file, "rb") as f:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=f
        )

    return response.text


# Example usage
# transcribed_text = speech_to_text("Recording.mp3")
# print("Transcribed Text:", transcribed_text)


def record_audio(filename, duration=10, sample_rate=44100):
    print("Recording...")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype="int16")
    sd.wait()
    write(filename, sample_rate, audio_data)
    print("Recording saved as", filename)

# Record for 5 seconds and transcribe
record_audio("live_audio.wav", duration=5)
transcribed_text = speech_to_text("live_audio.wav")
print("Transcribed Text:", transcribed_text)


