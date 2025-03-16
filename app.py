import streamlit as st
import boto3
import os
import time
from datetime import datetime
from streamlit_mic_recorder import mic_recorder
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
AWS_REGION = os.getenv("AWS_REGION")
AWS_TRANSCRIBE_ROLE_ARN = os.getenv("AWS_TRANSCRIBE_ROLE_ARN")  # IAM Role ARN for AWS Transcribe

# Initialize Boto3 clients
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION,
)

transcribe_client = boto3.client(
    "transcribe",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION,
)

# Function to upload file to S3
def upload_to_s3(file_path, file_name):
    try:
        s3_client.upload_file(file_path, AWS_BUCKET_NAME, file_name)
        return f"s3://{AWS_BUCKET_NAME}/{file_name}"
    except Exception as e:
        return f"❌ Error uploading file: {e}"

# Function to start transcription job
def start_transcription(s3_uri):
    job_name = f"transcribe_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    try:
        transcribe_client.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={"MediaFileUri": s3_uri},
            MediaFormat="wav",  # Change format if needed
            LanguageCode="en-US",
            OutputBucketName=AWS_BUCKET_NAME,
            OutputKey=f"{job_name}.json",
        )
        return job_name
    except Exception as e:
        return f"❌ Error starting transcription: {e}"

# Function to get transcription result
def get_transcription_text(job_name):
    while True:
        status = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        if status["TranscriptionJob"]["TranscriptionJobStatus"] in ["COMPLETED", "FAILED"]:
            break
        time.sleep(5)  # Wait before checking again

    if status["TranscriptionJob"]["TranscriptionJobStatus"] == "COMPLETED":
        transcript_uri = status["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
        return transcript_uri
    else:
        return "❌ Transcription failed."

# Streamlit UI
st.title("🎤 Voice Recorder & Transcriber")
st.write("Record your voice, upload it to AWS S3, and transcribe it to text.")

# Audio Recording
audio = mic_recorder(start_prompt="🎙️ Start Recording", stop_prompt="🛑 Stop Recording")

if audio and audio["bytes"]:
    st.audio(audio["bytes"], format="audio/wav")

    # Save audio file locally
    file_name = f"recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
    with open(file_name, "wb") as audio_file:
        audio_file.write(audio["bytes"])

    # Upload file to S3
    if st.button("Upload & Transcribe"):
        s3_uri = upload_to_s3(file_name, file_name)
        st.success(f"✅ File uploaded to: {s3_uri}")

        # Start Transcription
        job_name = start_transcription(s3_uri)
        st.write(f"⏳ Transcribing... (Job Name: {job_name})")
        
        # Fetch Transcription Result
        transcription_url = get_transcription_text(job_name)
        st.write("✅ Transcription Complete!")
        st.write(f"[View Transcription JSON]({transcription_url})")
