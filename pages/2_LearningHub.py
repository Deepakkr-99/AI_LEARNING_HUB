import streamlit as st
from utils.helper import load_lottie_url

st.set_page_config(page_title="AI Mentor", page_icon="🤖", layout="wide")

st.markdown("<h1 style='color:white;'>🤖 AI Mentor Hub</h1>", unsafe_allow_html=True)
load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_w51pcehl.json", height=200)

question = st.text_area("💬 Ask your AI Mentor:")
if st.button("🚀 Ask AI") and question.strip() != "":
    from utils.ai_agent import ask_ai
    with st.spinner("AI is thinking..."):
        answer = ask_ai(question)
        st.markdown(f"<p style='color:white;'>{answer}</p>", unsafe_allow_html=True)
