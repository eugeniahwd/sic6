import streamlit as st
import requests
import speech_recognition as sr
import re

# Fungsi untuk mengonversi audio ke teks menggunakan SpeechRecognition
def audio_to_text_using_recognition(audio_file):
    recognizer = sr.Recognizer()
    
    # Membaca file audio yang di-upload
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)  # Mengambil data audio dari file
        # Menggunakan Google Speech-to-Text dengan bahasa Indonesia
        text = recognizer.recognize_google(audio_data, language="id-ID")
    return text

# Fungsi untuk membersihkan teks dari karakter yang tidak diinginkan
def clean_text(text):
    # Menghapus karakter yang tidak diinginkan (misalnya, karakter acak atau simbol)
    text = re.sub(r'[^\x00-\x7F]+', '', text)  # Menghapus karakter non-ASCII
    text = re.sub(r'\s+', ' ', text)  # Mengganti spasi berlebih menjadi satu
    return text.strip()

# Fungsi untuk mengirim teks ke model LLaMA-3.2-3B-Instruct di Hugging Face
def get_llama_response(text):
    # Mengambil API key dari Streamlit Secrets
    huggingface_api_key = st.secrets["huggingface"]["api_key"]
    
    headers = {
        "Authorization": f"Bearer {huggingface_api_key}"
    }
    payload = {
        "inputs": text
    }
    
    url = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.2-3B-Instruct"
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        
        # Memeriksa status dan mencetak untuk debugging
        st.write(f"Status Code: {response.status_code}")
        st.write(f"Response Text: {response.text}")
        
        if response.status_code == 200:
            # Mengambil item pertama dari list respons dan membersihkan teksnya
            result = response.json()
            if isinstance(result, list):
                # Ambil teks yang dihasilkan dan bersihkan
                generated_text = result[0].get('generated_text', 'Tidak ada respons')
                cleaned_text = clean_text(generated_text)
                return {"generated_text": cleaned_text}
            else:
                return {"generated_text": "Unexpected response format"}
        else:
            return {"generated_text": "Error: Unable to get response from LLaMA"}
    
    except Exception as e:
        st.write(f"Error occurred: {e}")
        return {"generated_text": "An error occurred while processing the request."}

# Membuat tampilan Streamlit
st.title("Audio to LLaMA Response")

# File uploader untuk merekam audio
audio_file = st.file_uploader("Upload Audio", type=["wav", "mp3"])

if audio_file is not None:
    # Mengonversi audio ke teks
    st.write("Mengenali teks dari audio...")
    
    try:
        # Menggunakan speech recognition untuk mengonversi audio ke teks
        text = audio_to_text_using_recognition(audio_file)
        st.write(f"Teks: {text}")
        
        # Mengirim teks ke LLaMA dan mendapatkan respons
        response = get_llama_response(text)
        
        # Menampilkan respons dari LLaMA
        st.write("Respons dari LLaMA:")
        st.write(response.get('generated_text', 'Tidak ada respons'))
    
    except Exception as e:
        st.write(f"Terjadi kesalahan saat memproses audio: {e}")
