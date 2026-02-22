import streamlit as st
import requests
import streamlit.components.v1 as components

st.set_page_config(page_title="AI Mentor", page_icon="🤖", layout="centered")

# 🔐 Login check
if "username" not in st.session_state:
    st.warning("Please login first")
    st.stop()

# ---------------- Gemini Config ----------------
MODEL_NAME = "gemini-2.5-flash"
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

def ask_ai(question: str) -> str:
    try:
        url = f"https://generativelanguage.googleapis.com/v1/models/{MODEL_NAME}:generateContent?key={GEMINI_API_KEY}"
        headers = {"Content-Type": "application/json"}
        data = {"contents": [{"parts": [{"text": question}]}]}

        response = requests.post(url, headers=headers, json=data, timeout=20)

        if response.status_code != 200:
            return f"⚠ Gemini API Error"

        result = response.json()
        candidates = result.get("candidates")

        if candidates:
            return candidates[0]["content"]["parts"][0]["text"]

        return "⚠ No response generated."

    except Exception:
        return "⚠ Error while generating response"


# ---------------- UI Styling ----------------
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

# ---------------- Voice Input ----------------
components.html("""
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
        document.getElementById('output').innerText =
            event.results[0][0].transcript;
        window.parent.postMessage(
            {type: "streamlit:setComponentValue", value: event.results[0][0].transcript},
            "*"
        );
    };
}
</script>
""", height=200)

# ---------------- Text Input ----------------
question = st.text_area("Ask your AI Mentor")

if st.button("🚀 Ask AI"):
    if question.strip() == "":
        st.warning("Enter question first")
    else:
        with st.spinner("AI is thinking..."):
            answer = ask_ai(question)
            st.success("AI Response")
            st.write(answer)
