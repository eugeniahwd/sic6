import streamlit as st

st.title("Eugenia's Website")
st.write("Welcome to my web!")

prompt = st.chat_input("Say something")
if prompt:
    st.write(f"User: {prompt}")

st.balloons()

st.badge("New")
st.badge("Success", icon=":material/check:", color="green")

st.markdown(
    ":violet-badge[:material/star: Favorite] :orange-badge[⚠️ Needs review] :gray-badge[Deprecated]"
)
