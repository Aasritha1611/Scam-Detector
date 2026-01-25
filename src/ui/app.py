import streamlit as st
import requests

st.title("AI Job Scam Detector")

text = st.text_area("Paste job/internship message")

if st.button("Analyze"):
    res = requests.post(
        "http://127.0.0.1:8000/predict",
        json={"text": text}
    ).json()

    st.write(res)
    