import streamlit as st
import requests

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="AI Text Mentor", page_icon="🤖", layout="centered")

# ---------- LOGIN CHECK ----------
if "username" not in st.session_state:
    st.warning("Please login first")
    st.stop()

# ---------- GEMINI CONFIG ----------
MODEL_NAME = "gemini-2.5-flash"
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

def ask_ai(question: str) -> str:
    """
    Send question to Gemini API and get AI response.
    """
    try:
        url = f"https://generativelanguage.googleapis.com/v1/models/{MODEL_NAME}:generateContent?key={GEMINI_API_KEY}"
        headers = {"Content-Type": "application/json"}
        data = {"contents": [{"parts": [{"text": question}]}]}

        response = requests.post(url, headers=headers, json=data, timeout=20)

        if response.status_code != 200:
            return "⚠ Gemini API Error"

        result = response.json()
        candidates = result.get("candidates")

        if candidates:
            return candidates[0]["content"]["parts"][0]["text"]

        return "⚠ No response generated."

    except Exception:
        return "⚠ Error while generating response"

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg,#1f1c2c,#928dab);
}
.title {
    text-align:center;
    font-size:32px;
    font-weight:700;
    margin-bottom:20px;
}
.stButton>button {
    border-radius:25px;
    padding:10px 25px;
    background: linear-gradient(90deg,#00c6ff,#0072ff);
    color:white;
    font-weight:600;
    border:none;
    transition:0.3s;
}
.stButton>button:hover {
    transform: scale(1.08);
    box-shadow:0 0 20px #00c6ff;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🤖 AI Text Mentor</div>', unsafe_allow_html=True)

# ---------- TEXT INPUT ----------
question = st.text_area("Ask your AI Mentor:")

# ---------- ASK BUTTON ----------
if st.button("🚀 Ask AI"):
    if question.strip() == "":
        st.warning("Please enter a question first.")
    else:
        with st.spinner("AI is thinking... 🤖"):
            answer = ask_ai(question)
            st.success("AI Response")
            st.write(answer)
