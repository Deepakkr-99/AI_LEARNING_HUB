import streamlit as st
from utils.ai_agent import ask_ai, listen_to_speech

st.set_page_config(page_title="Learning Hub", page_icon="📚", layout="centered")

if "username" not in st.session_state:
    st.warning("Please login first")
    st.stop()

st.title("📚 Learning Hub - AI Mentor")

# --- Voice Input ---
st.markdown("### 🎤 Talk to Your AI Mentor")
if st.button("Speak to Mentor"):
    question = listen_to_speech()
    if question:
        st.info(f"You said: {question}")
        answer = ask_ai(question)
        st.text_area("Mentor says:", answer, height=200)
    else:
        st.warning("No voice recognized. Try again!")

# --- Or type manually ---
st.markdown("---")
question = st.text_area("Or type your question:", value="")
if st.button("🚀 Ask AI"):
    if question.strip() == "":
        st.warning("Enter or speak a question first.")
    else:
        answer = ask_ai(question)
        st.text_area("Mentor says:", answer, height=200)
