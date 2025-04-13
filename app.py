import openai
import streamlit as st

# Masukkan API Key dari OpenAI
openai.api_key = "YOUR_OPENAI_API_KEY"  # Ganti dengan API Key Anda

# Fungsi untuk mendapatkan respons dari GPT
def get_openai_response(text):
    response = openai.Completion.create(
        model="text-davinci-003",  # Gunakan "gpt-4" jika Anda ingin menggunakan GPT-4
        prompt=text,
        max_tokens=20  # Jumlah token maksimum yang ingin digunakan
    )
    return response.choices[0].text.strip()

# Membuat tampilan Streamlit
st.title("Menggunakan GPT-3.5 atau GPT-4 untuk Membuat Respons")

# Input teks untuk prompt
user_input = st.text_area("Masukkan teks untuk mendapatkan respons GPT")

# Ketika pengguna mengirimkan teks
if user_input:
    st.write("Mengenali teks dari input...")

    # Dapatkan respons dari GPT
    gpt_response = get_openai_response(user_input)

    # Menampilkan respons dari GPT
    st.write("Respons dari GPT-3.5 atau GPT-4:")
    st.write(gpt_response)
