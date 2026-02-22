import streamlit as st
import requests
import streamlit.components.v1 as components

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="AI Mentor", page_icon="🤖", layout="centered")

# ---------- LOGIN CHECK ----------
if "username" not in st.session_state:
    st.warning("Please login first")
    st.stop()

# ---------- GEMINI CONFIG ----------
MODEL_NAME = "gemini-2.5-flash"
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

def ask_ai(question: str) -> str:
    """
    Send question to Gemini API and return AI response.
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

    except Exception as e:
        return f"⚠ Error: {str(e)}"

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg,#1f1c2c,#928dab);
}
.title {
    text-align:center;
    font-size:34px;
    font-weight:800;
    margin-bottom:25px;
    color:#00c6ff;
}
.stTextArea>div>div>textarea {
    font-size:16px;
    padding:12px;
    border-radius:12px;
    border:1px solid #00c6ff;
    background-color:#1f1c2c;
    color:white;
}
.stButton>button {
    border-radius:25px;
    padding:12px 28px;
    background: linear-gradient(90deg,#00c6ff,#0072ff);
    color:white;
    font-weight:700;
    border:none;
    transition:0.3s;
}
.stButton>button:hover {
    transform: scale(1.05);
    box-shadow:0 0 20px #00c6ff;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🎤 AI Voice & Text Mentor</div>', unsafe_allow_html=True)

# ---------- VOICE INPUT COMPONENT ----------
voice_text = components.html("""
<div style="text-align:center;">
    <button onclick="startDictation()" 
    style="padding:12px 25px;border-radius:30px;
    background:linear-gradient(90deg,#ff9966,#ff5e62);
    color:white;border:none;font-size:16px;
    font-weight:600;">
    🎙️ Speak Now
    </button>
    <p id="status" style="margin-top:10px;color:white;font-weight:600;"></p>
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
        window.parent.postMessage(
            {type: "streamlit:setComponentValue", value: text},
            "*"
        );
    };

    recognition.onerror = function() {
        document.getElementById("status").innerHTML = "Mic error ❌";
    };
}
</script>
""", height=180)

# ---------- TEXT AREA ----------
question = st.text_area("Ask your AI Mentor:", value=voice_text or "")

# ---------- ASK AI BUTTON ----------
if st.button("🚀 Ask AI"):
    if not question.strip():
        st.warning("Please enter a question or use the microphone.")
    else:
        with st.spinner("AI is thinking... 🤖"):
            answer = ask_ai(question)
            st.success("AI Response")
            st.write(answer)
