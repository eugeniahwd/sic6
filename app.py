import streamlit as st
import requests
import speech_recognition as sr
from io import BytesIO

# Fungsi untuk mengonversi audio ke teks menggunakan SpeechRecognition
def audio_to_text_using_recognition(audio_file):
    recognizer = sr.Recognizer()
    
    # Membaca file audio yang di-upload
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)  # Mengambil data audio dari file
        text = recognizer.recognize_google(audio_data, language="id-ID")  # Menggunakan Google Speech-to-Text dengan bahasa Indonesia
    return text

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
    try:
        text = audio_to_text_using_recognition(audio_file)
        st.write(f"Teks: {text}")
    except Exception as e:
        st.write(f"Terjadi kesalahan saat memproses audio: {e}")
    
    # Mengirim teks ke LLaMA dan mendapatkan respons
    if text:
        response = get_llama_response(text)
        
        # Menampilkan respons dari LLaMA
        st.write("Respons dari LLaMA:")
        st.write(response.get('generated_text', 'Tidak ada respons'))
