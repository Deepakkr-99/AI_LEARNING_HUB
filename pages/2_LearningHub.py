import streamlit as st
import google.generativeai as genai
import speech_recognition as sr

st.set_page_config(page_title="AI Learning Hub", page_icon="📘", layout="wide")

# 🔐 Login Check
if "username" not in st.session_state:
    st.warning("Please login first to use AI Mentor")
    st.stop()

username = st.session_state["username"]

st.title("📘 AI Learning Hub")
st.markdown(f"### 👋 Welcome {username}, Ask your AI Mentor anything!")

# 🔐 Load Gemini API
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception:
    st.error("❌ Gemini API Key missing or invalid")
    st.stop()

model = genai.GenerativeModel("gemini-2.5-flash")

# ---------------- Voice Input Function ----------------
def voice_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙 Listening... Speak now")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        return text
    except:
        return None

# ---------------- Input Section ----------------
col1, col2 = st.columns([4,1])

with col1:
    question = st.text_area("💬 Ask your AI Mentor:")

with col2:
    if st.button("🎙 Voice"):
        voice_text = voice_to_text()
        if voice_text:
            st.success("Voice Captured!")
            question = voice_text
            st.session_state["voice_question"] = voice_text
        else:
            st.error("Voice not recognized")

# If voice was captured earlier
if "voice_question" in st.session_state:
    question = st.session_state["voice_question"]
    st.write("🗣 You said:", question)

# ---------------- Ask AI ----------------
if st.button("🚀 Ask AI"):
    if question.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.spinner("🤖 AI is thinking..."):
            try:
                response = model.generate_content(question)

                st.markdown("## 🤖 AI Mentor Response")
                st.success("Here is your answer:")
                st.write(response.text)

            except Exception:
                st.error("❌ Error while generating response")
