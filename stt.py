import streamlit as st
import sounddevice as sd
from scipy.io.wavfile import write
import openai
import os
from pathlib import Path
import numpy as np
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Create a directory for storing audio files if it doesn't exist
AUDIO_DIR = Path("recorded_audio")
AUDIO_DIR.mkdir(exist_ok=True)


def record_audio(duration, sample_rate=44100):
    """Record audio for the specified duration"""
    recording = sd.rec(int(duration * sample_rate),
                       samplerate=sample_rate,
                       channels=1,
                       dtype='int16')
    sd.wait()
    return recording, sample_rate


def save_audio(recording, sample_rate, filename):
    """Save the recorded audio to a WAV file"""
    write(filename, sample_rate, recording)


def transcribe_audio(audio_path):
    """Transcribe audio using OpenAI Whisper"""
    try:
        with open(audio_path, "rb") as audio_file:
            response = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        return response.text
    except Exception as e:
        return f"Error during transcription: {str(e)}"


# Streamlit UI
st.title("Voice Recording and Transcription App")

# Recording duration slider
duration = st.slider("Recording Duration (seconds)", 1, 30, 5)

# Initialize session state for recording status
if 'recording_status' not in st.session_state:
    st.session_state['recording_status'] = False

if 'transcribed_text' not in st.session_state:
    st.session_state['transcribed_text'] = ""

# Recording button
col1, col2 = st.columns(2)

with col1:
    if st.button("Start Recording"):
        if not st.session_state['recording_status']:
            st.session_state['recording_status'] = True
            # Create a unique filename
            filename = AUDIO_DIR / f"recording_{np.random.randint(10000)}.wav"

            # Show recording status
            with st.spinner(f"Recording for {duration} seconds..."):
                # Record and save audio
                recording, sample_rate = record_audio(duration)
                save_audio(recording, sample_rate, filename)
                st.success(f"Recording saved!")

            # Transcribe the audio
            with st.spinner("Transcribing audio..."):
                transcribed_text = transcribe_audio(filename)
                st.session_state['transcribed_text'] = transcribed_text
                st.success("Transcription complete!")

            st.session_state['recording_status'] = False

# Display transcribed text
if st.session_state['transcribed_text']:
    st.header("Transcription")
    st.write(st.session_state['transcribed_text'])