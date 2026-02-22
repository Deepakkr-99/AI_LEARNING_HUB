import streamlit as st
import requests
import streamlit.components.v1 as components

MODEL_NAME = "gemini-2.5-flash"
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")

def ask_ai(question: str) -> str:
    """
    Send question to Gemini API and get AI response.
    """
    if not GEMINI_API_KEY:
        return "⚠ GEMINI_API_KEY not found in secrets."

    try:
        url = f"https://generativelanguage.googleapis.com/v1/models/{MODEL_NAME}:generateContent?key={GEMINI_API_KEY}"
        headers = {"Content-Type": "application/json"}
        data = {"contents": [{"parts": [{"text": question}]}]}

        response = requests.post(url, headers=headers, json=data, timeout=20)
        if response.status_code != 200:
            return f"⚠ Gemini API Error: {response.text}"

        result = response.json()
        candidates = result.get("candidates")
        if candidates:
            content = candidates[0].get("content")
            if content:
                parts = content[0].get("parts")
                if parts:
                    return parts[0].get("text", "⚠ No text found")
        return "⚠ No response generated."

    except Exception as e:
        return f"⚠ Error: {str(e)}"


def listen_to_speech() -> str:
    """
    Streamlit HTML/JS component to capture voice input and return as text.
    """
    if "voice_text" not in st.session_state:
        st.session_state.voice_text = ""

    voice_text = components.html("""
    <div style="text-align:center;">
        <button onclick="startDictation()" 
        style="padding:12px 25px;border-radius:30px;
        background:linear-gradient(90deg,#ff9966,#ff5e62);
        color:white;border:none;font-size:16px;
        font-weight:600;">
        🎙️ Speak Now
        </button>
        <p id="status" style="margin-top:10px;color:white;"></p>
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

    if voice_text:
        st.session_state.voice_text = voice_text

    return st.session_state.voice_text
