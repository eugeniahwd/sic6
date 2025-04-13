import streamlit as st
import requests
from io import BytesIO
from pydub import AudioSegment
import whisper
import json

# Inisialisasi Whisper model untuk STT
whisper_model = whisper.load_model("base")

# Fungsi untuk mengonversi audio ke teks menggunakan Whisper
def audio_to_text(audio_file):
    audio = AudioSegment.from_file(audio_file)
    audio = audio.set_channels(1).set_frame_rate(16000)
    audio_data = audio.raw_data

    result = whisper_model.transcribe(audio_data)
    return result["text"]

# Fungsi untuk mengirim teks ke model LLaMA di Hugging Face
def get_llama_response(text):
    # Mengambil API key dari Streamlit Secrets
    huggingface_api_key = st.secrets["huggingface"]["api_key"]
    
    headers = {
        "Authorization": f"Bearer {huggingface_api_key}"
    }
    payload = {
        "inputs": text
    }
    response = requests.post(
        "https://api-inference.huggingface.co/models/meta-llama/Llama-3.2-3B-Instruct",
        headers=headers,
        json=payload
    )
    return response.json()

# Membuat tampilan Streamlit
st.title("Audio to LLaMA Response")

# File uploader untuk merekam audio
audio_file = st.file_uploader("Upload Audio", type=["wav", "mp3"])

if audio_file is not None:
    # Mengonversi audio ke teks
    st.write("Mengenali teks dari audio...")
    text = audio_to_text(audio_file)
    st.write(f"Teks: {text}")
    
    # Mengirim teks ke LLaMA dan mendapatkan respons
    response = get_llama_response(text)
    
    # Menampilkan respons dari LLaMA
    st.write("Respons dari LLaMA:")
    st.write(response.get('generated_text', 'Tidak ada respons'))
