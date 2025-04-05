import streamlit as st
from detect import detect_faces_and_eyes
from PIL import Image
import numpy as np

st.title("Face and Eye Detection with YOLO")
uploaded_file = st.file_uploader("Upload a photo", type=["jpg", "png", "jpeg"])

if uploaded_file:
    st.subheader("Original Image", divider="violet")
    img = Image.open(uploaded_file).convert("RGB")
    st.image(img,  use_container_width=True)

    st.subheader("Original Image", divider="blue")
    result_img = detect_faces_and_eyes(np.array(img))
    st.image(result_img,  use_container_width=True)
