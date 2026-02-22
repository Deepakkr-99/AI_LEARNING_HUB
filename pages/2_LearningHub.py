import sys
import os

# Fix for ModuleNotFoundError
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from ai_agent import ask_ai
import streamlit.components.v1 as components

st.set_page_config(page_title="AI Mentor", page_icon="🤖", layout="centered")

# Login check
if "username" not in st.session_state:
    st.warning("Please login first")
    st.stop()

# Session state
if "question" not in st.session_state:
    st.session_state.question = ""
if "answer" not in st.session_state:
    st.session_state.answer = ""

# Custom CSS
st.markdown("""
<style>
body { background: linear-gradient(135deg,#1f1c2c,#928dab); }
.title { text-align:center; font-size:34px; font-weight:800; margin-bottom:25px; color:#00c6ff; }
.stTextArea>div>div>textarea { font-size:16px; padding:12px; border-radius:12px; border:1px solid #00c6ff; background-color:#1f1c2c; color:white; }
.stButton>button { border-radius:25px; padding:12px 28px; background: linear-gradient(90deg,#00c6ff,#0072ff); color:white; font-weight:700; border:none; transition:0.3s; }
.stButton>button:hover { transform: scale(1.05); box-shadow:0 0 20px #00c6ff; }
.status-text { color:white; font-weight:600; margin-top:10px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🎤 AI Voice & Text Mentor</div>', unsafe_allow_html=True)

# Voice Input
voice_text = components.html("""
<div style="text-align:center;">
    <button onclick="startDictation()" style="padding:12px 25px;border-radius:30px;
    background:linear-gradient(90deg,#ff9966,#ff5e62); color:white;border:none;font-size:16px;font-weight:600;">
    🎙️ Speak Now
    </button>
    <p id="status" class="status-text"></p>
</div>
<script>
function startDictation() {
    var recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'en-IN';
    recognition.start();
    document.getElementById("status").innerHTML = "Listening... 🎧";
    recognition.onresult = function(event) {
        var text = event.results[0][0].transcript;
        document.getElementById("status").innerHTML = "You said: " + text;
        window.parent.postMessage({type: "streamlit:setComponentValue", value: text},"*");
    };
    recognition.onerror = function() { document.getElementById("status").innerHTML = "Mic error ❌"; }
}
</script>
""", height=180)

# Text Area
question_input = st.text_area("Ask your AI Mentor:", value=st.session_state.question)
st.session_state.question = question_input

# Ask AI Button
if st.button("🚀 Ask AI"):
    if not st.session_state.question.strip():
        st.warning("Please enter a question or use the microphone.")
    else:
        with st.spinner("AI is thinking... 🤖"):
            st.session_state.answer = ask_ai(st.session_state.question)
            st.success("AI Response")
            st.write(st.session_state.answer)
