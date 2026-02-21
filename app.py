import streamlit as st

# ---------- Page Config ----------
st.set_page_config(
    page_title="NeuroSpark AI",
    page_icon="🧠",
    layout="wide"
)

# ---------- Custom CSS ----------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Poppins', sans-serif;
    }

    body {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    }

    .main-container {
        background: rgba(255, 255, 255, 0.08);
        padding: 40px;
        border-radius: 20px;
        backdrop-filter: blur(15px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.37);
        text-align: center;
        margin-top: 50px;
    }

    .main-title {
        font-size: 48px;
        font-weight: 700;
        color: #ffffff;
    }

    .subtitle {
        font-size: 20px;
        color: #e0e0e0;
        margin-top: 15px;
    }

    .feature-list {
        text-align: left;
        font-size: 18px;
        margin-top: 25px;
        color: #ffffff;
    }

    .stButton>button {
        border-radius: 30px;
        padding: 10px 30px;
        background: linear-gradient(90deg, #00c6ff, #0072ff);
        color: white;
        font-weight: 600;
        border: none;
        transition: 0.3s ease-in-out;
    }

    .stButton>button:hover {
        transform: scale(1.08);
        box-shadow: 0px 0px 20px #00c6ff;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- UI Layout ----------
st.markdown("""
<div class="main-container">
    <div class="main-title">🧠 NeuroSpark AI</div>
    <div class="subtitle">
        Your Intelligent Learning Companion for Smarter Growth 🚀
    </div>
    <div class="feature-list">
        ✔ Login / Sign Up <br>
        ✔ Smart Dashboard <br>
        ✔ AI Mentor Hub <br>
        ✔ Interactive Quizzes <br>
        ✔ Progress Tracking <br>
        ✔ Personal Settings
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------- Get Started Button ----------
if st.button("✨ Get Started"):
    st.switch_page("0_Login")  # pages/0_Login.py ke liye exact name


