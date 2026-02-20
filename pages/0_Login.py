import streamlit as st
from utils.auth_manager import login_user, register_user
from utils.helper import load_lottie_url

st.set_page_config(page_title="Login - NeuroSpark AI", page_icon="🔐", layout="centered")

# ---------- Custom CSS ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

html, body, [class*="css"]  {
    font-family: 'Poppins', sans-serif;
}

body {
    background: linear-gradient(135deg, #141e30, #243b55);
}

.login-card {
    background: rgba(255, 255, 255, 0.08);
    padding: 40px;
    border-radius: 20px;
    backdrop-filter: blur(15px);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.37);
}

.stTextInput>div>div>input {
    border-radius: 10px;
}

.stButton>button {
    width: 100%;
    border-radius: 30px;
    padding: 10px;
    background: linear-gradient(90deg, #00c6ff, #0072ff);
    color: white;
    font-weight: 600;
    border: none;
    transition: 0.3s ease-in-out;
}

.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0px 0px 15px #00c6ff;
}
</style>
""", unsafe_allow_html=True)

# ---------- Title ----------
st.markdown("<h1 style='text-align:center; color:white;'>🔐 Welcome to NeuroSpark AI</h1>", unsafe_allow_html=True)

# ---------- Animation ----------
load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_jcikwtux.json", height=180)

# ---------- Login Card ----------
st.markdown("<div class='login-card'>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🔑 Login", "🆕 Sign Up"])

with tab1:
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login"):
        if login_user(username, password):
            st.session_state['username'] = username
            st.success("Login successful! Go to Dashboard from sidebar 🚀")
        else:
            st.error("Invalid Username or Password")

with tab2:
    new_user = st.text_input("New Username", key="signup_user")
    new_pass = st.text_input("New Password", type="password", key="signup_pass")

    if st.button("Create Account"):
        success, msg = register_user(new_user, new_pass)
        if success:
            st.success(msg)
        else:
            st.error(msg)

st.markdown("</div>", unsafe_allow_html=True)