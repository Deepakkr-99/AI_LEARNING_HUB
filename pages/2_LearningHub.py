# learning_hub.py
import streamlit as st
import streamlit.components.v1 as components
from ai_mentor import ask_ai  # import function from ai_mentor.py

st.set_page_config(page_title="AI Mentor", page_icon="🤖", layout="centered")

# Login check
if "username" not in st.session_state:
    st.warning("Please login first")
    st.stop()

# UI Styling
st.markdown("""
<style>
.title {
    text-align:center;
    font-size:32px;
    font-weight:700;
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

st.markdown('<div class="title">🤖 AI Voice Mentor</div>', unsafe_allow_html=True)

# Session state
if "question" not in st.session_state:
    st.session_state["question"] = ""

# Voice input
voice_input = components.html("""
<div style="text-align:center;">
    <button onclick="startDictation()" 
    style="padding:10px 20px;border-radius:20px;
    background:linear-gradient(90deg,#ff9966,#ff5e62);
    color:white;border:none;font-size:16px;">
    🎤 Start Voice Input
    </button>
    <p id="output" style="margin-top:10px;color:white;"></p>
</div>

<script>
function startDictation() {
    var recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'en-IN';
    recognition.start();

    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;
        document.getElementById('output').innerText = transcript;
        window.parent.postMessage(
            {type: "streamlit:setComponentValue", value: transcript},
            "*"
        );
    };
}
</script>
""", height=200, scrolling=False)

if voice_input:
    st.session_state["question"] = voice_input

# Text input
st.session_state["question"] = st.text_area(
    "Ask your AI Mentor",
    value=st.session_state["question"]
)

# Ask AI button
if st.button("🚀 Ask AI"):
    question = st.session_state["question"]
    if question.strip() == "":
        st.warning("Enter question first")
    else:
        with st.spinner("AI is thinking..."):
            answer = ask_ai(question)
            st.success("AI Response")
            st.write(answer)
