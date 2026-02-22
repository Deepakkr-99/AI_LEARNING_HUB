import sys
import os

# Fix ModuleNotFoundError: add root folder to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from ai_agent import ask_ai  # Now this works

# ---------------- Page Setup ----------------
st.set_page_config(page_title="AI Mentor", page_icon="🤖", layout="centered")

# 🔐 Login check
if "username" not in st.session_state:
    st.warning("Please login first")
    st.stop()

# ---------------- UI Styling ----------------
st.markdown("""
<style>
.title {
    text-align:center;
    font-size:32px;
    font-weight:700;
    color:#00c6ff;
}
.stButton>button {
    border-radius:25px;
    padding:10px 25px;
    background: linear-gradient(90deg,#00c6ff,#0072ff);
    color:white;
    font-weight:600;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🤖 AI Text Mentor</div>', unsafe_allow_html=True)

# ---------------- Text Input ----------------
question = st.text_area("Ask your AI Mentor")

# ---------------- Ask AI Button ----------------
if st.button("🚀 Ask AI"):
    if not question.strip():
        st.warning("Enter a question first")
    else:
        with st.spinner("AI is thinking..."):
            try:
                answer = ask_ai(question)
                st.success("AI Response")
                st.write(answer)
            except Exception as e:
                st.error(f"Error while fetching AI response: {str(e)}")
