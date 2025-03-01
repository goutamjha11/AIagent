import os
import sounddevice as sd
from scipy.io.wavfile import write
import streamlit as st
import whisper
from tempfile import NamedTemporaryFile
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Whisper model
model = whisper.load_model("base")  # You can use "small", "medium", or "large" models as needed.


# Function to transcribe audio using OpenAI's Whisper model
def speech_to_text(audio_file):
    # Transcribe the audio using Whisper
    result = model.transcribe(audio_file)
    return result["text"]


# Function to record audio using the microphone
def record_audio(filename, duration=5, sample_rate=44100):
    st.write("Recording audio...")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype="int16")
    sd.wait()
    write(filename, sample_rate, audio_data)
    st.write("Recording complete.")


# Streamlit UI setup
st.title("Speech-to-Text with OpenAI Whisper")

# User interface elements
record_button = st.button("Start Recording")
if record_button:
    # Record audio when the button is pressed
    with st.spinner("Recording... Please wait."):
        temp_audio_file = NamedTemporaryFile(delete=False, suffix=".wav")
        record_audio(temp_audio_file.name, duration=5)

    # Display the recorded audio file path
    st.audio(temp_audio_file.name)

    # Transcribe the audio using Whisper
    st.write("Transcribing the audio...")
    try:
        transcribed_text = speech_to_text(temp_audio_file.name)
        st.success("Transcription successful!")
        st.write("Transcribed Text: ", transcribed_text)
    except Exception as e:
        st.error(f"Error during transcription: {e}")
