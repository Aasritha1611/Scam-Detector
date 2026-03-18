import streamlit as st
import requests

# Professional UI setup
st.set_page_config(page_title="Scam Detector", page_icon="🚫", layout="centered")

st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .title-text {
        color: #2c3e50;
        text-align: center;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .subtitle-text {
        color: #34495e;
        text-align: center;
        font-size: 1.1em;
        margin-bottom: 2em;
    }
    .stTextArea textarea {
        border-radius: 10px !important;
        border: 1px solid #ced4da !important;
        padding: 15px !important;
        font-size: 1em !important;
    }
    div.stButton > button {
        background-color: #3498db;
        color: white;
        border-radius: 8px;
        padding: 10px 24px;
        border: none;
        font-weight: bold;
        width: 100%;
        transition: all 0.3s;
    }
    div.stButton > button:hover {
        background-color: #2980b9;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .result-card {
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .safe-card {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        color: #155724;
    }
    .scam-card {
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
        color: #721c24;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='title-text'>🚫 Scam Detector</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle-text'>Analyze messages, news, or links to instantly detect potential scams and fake news.</p>", unsafe_allow_html=True)

text = st.text_area("Paste the content to analyze below:", height=150, placeholder="E.g., Congratulations! You won a $1000 gift card. Click here to claim your prize...")

if st.button("Analyze Content"):
    if not text.strip():
        st.warning("Please enter some text to analyze.")
    else:
        with st.spinner("Analyzing content..."):
            try:
                res = requests.post(
                    "http://127.0.0.1:8000/predict",
                    json={"text": text}
                )
                if res.status_code == 200:
                    data = res.json()
                    
                    # Showing results
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Trust Score", f"{data['trust_score']}%")
                    with col2:
                        st.metric("Scam Probability", f"{data['scam_probability']}%")
                        
                    # Notification system
                    if data['is_scam']:
                        st.error("🚨 " + data['message'])
                        st.markdown(f"<div class='result-card scam-card'><h3>Unauthorized / False Content Detected</h3><p>This content exhibits high characteristics of a scam or fake news. Exercise extreme caution.</p></div>", unsafe_allow_html=True)
                    else:
                        st.success("✅ " + data['message'])
                        st.markdown(f"<div class='result-card safe-card'><h3>Content Appears Safe</h3><p>No major indicators of scams or fake news were found.</p></div>", unsafe_allow_html=True)
                else:
                    st.error("Error connecting to the analysis server.")
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the backend server. Make sure it is running.")