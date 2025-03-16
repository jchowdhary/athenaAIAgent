import streamlit as st
import boto3
import asyncio
import websockets
import json
import sounddevice as sd
import numpy as np
from dotenv import load_dotenv
import os

# Load AWS credentials from .env file
load_dotenv()
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")

# Initialize AWS Transcribe Streaming Client
transcribe_client = boto3.client(
    'transcribe',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

# Streamlit UI
st.title("🎙️ Real-Time Speech to Text with AWS Transcribe")
st.write("Click the button below to start recording and transcribing in real-time.")

if "transcription" not in st.session_state:
    st.session_state.transcription = ""

# AWS WebSocket URL for Transcribe
TRANSCRIBE_WEBSOCKET_URL = f"wss://transcribestreaming.{AWS_REGION}.amazonaws.com:8443"

# Audio settings
SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK_DURATION_MS = 100
CHUNK_SIZE = int(SAMPLE_RATE * CHUNK_DURATION_MS / 1000)

async def transcribe_stream():
    async with websockets.connect(TRANSCRIBE_WEBSOCKET_URL) as websocket:
        print("Connected to AWS Transcribe WebSocket")

        # Send start request
        start_request = {
            "ContentType": "audio/x-l16; rate=16000",
            "LanguageCode": "en-US"
        }
        await websocket.send(json.dumps(start_request))

        # Function to capture audio and send to AWS Transcribe
        def audio_callback(indata, frames, time, status):
            if status:
                print(f"Audio error: {status}")
            audio_data = (indata * 32767).astype(np.int16).tobytes()
            asyncio.run_coroutine_threadsafe(websocket.send(audio_data), asyncio.get_event_loop())

        # Start recording
        with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, callback=audio_callback, dtype="int16"):
            st.write("🎤 **Recording... Speak now!**")
            await asyncio.sleep(30)  # 30 seconds of recording

        # Listen for transcribed text
        async for message in websocket:
            response = json.loads(message)
            if "Transcript" in response:
                transcript = response["Transcript"]["Results"]
                for result in transcript:
                    if "Alternatives" in result:
                        text = result["Alternatives"][0]["Transcript"]
                        if text.strip():
                            st.session_state.transcription += text + "\n"
                            st.write(f"📝 **Live Transcription:** {text}")

# Streamlit Button to Start Transcription
if st.button("🎤 Start Recording & Transcribe"):
    asyncio.run(transcribe_stream())

# Display Final Transcription
if st.session_state.transcription:
    st.subheader("📝 Final Transcription")
    st.text_area("Transcribed Text", st.session_state.transcription, height=200)
    st.download_button("⬇️ Download Transcription", st.session_state.transcription, file_name="transcription.txt")
