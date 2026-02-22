import streamlit as st

# ---------- Page Config ----------
st.set_page_config(
    page_title="NeuroSpark AI",
    page_icon="🧠",
    layout="wide"
)

# ---------- Redirect ----------
if st.session_state.get("goto_login"):
    st.switch_page("pages/0_Login.py")

# ---------- Custom CSS ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&family=Poppins:wght@300;400;600&display=swap');

body {
    background: linear-gradient(-45deg, #141e30, #243b55, #1f4037, #99f2c8);
    background-size: 400% 400%;
    animation: gradientBG 12s ease infinite;
}

@keyframes gradientBG {
    0% {background-position:0% 50%}
    50% {background-position:100% 50%}
    100% {background-position:0% 50%}
}

.hero-card {
    margin-top:70px;
    padding:60px;
    border-radius:25px;
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(18px);
    box-shadow: 0 8px 40px rgba(0,0,0,0.4);
    text-align:center;
    animation: floatCard 4s ease-in-out infinite;
}

@keyframes floatCard {
    0% {transform: translateY(0px);}
    50% {transform: translateY(-10px);}
    100% {transform: translateY(0px);}
}

.main-title {
    font-family: 'Orbitron', sans-serif;
    font-size:56px;
    font-weight:700;
    background: linear-gradient(90deg,#00f2fe,#4facfe);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    font-family: 'Poppins', sans-serif;
    font-size:22px;
    color:#ffffff;
    margin-top:20px;
}

.features {
    margin-top:30px;
    font-size:18px;
    color:#ffffff;
    line-height:1.8;
}

.stButton>button {
    margin-top:30px;
    border-radius:40px;
    padding:14px 45px;
    font-size:18px;
    font-weight:600;
    background: linear-gradient(90deg,#ff9966,#ff5e62);
    color:white;
    border:none;
    transition: all 0.4s ease;
}

.stButton>button:hover {
    transform: scale(1.1);
    box-shadow: 0 0 25px #ff5e62;
}
</style>
""", unsafe_allow_html=True)

# ---------- Hero Section ----------
st.markdown("""
<div class="hero-card">
    <div class="main-title">🧠 NeuroSpark AI</div>
    <div class="subtitle">Your Intelligent Learning Companion for Smarter Growth 🚀</div>
    <div class="features">
        ✔ Secure Login & Register <br>
        ✔ AI Mentor Assistance <br>
        ✔ Interactive Smart Quizzes <br>
        ✔ Performance Dashboard <br>
        ✔ AI Score Prediction <br>
        ✔ Advanced Progress Tracking
    </div>
</div>
""", unsafe_allow_html=True)

# ---------- Button ----------
if st.button("🚀 Get Started"):
    st.session_state["goto_login"] = True
    st.switch_page("pages/0_Login.py")
