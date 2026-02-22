import streamlit as st
from streamlit_webrtc import webrtc_streamer
import requests
import tempfile
import speech_recognition as sr
import numpy as np
import av

st.set_page_config(page_title="🎤 Voice to Gemini AI", layout="wide")
st.title("🎤 Voice to Gemini AI")
st.write("Speak into your mic and get AI response!")

MODEL_NAME = "gemini-2.5-flash"
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

# -----------------------
# Function to call Gemini API
# -----------------------
def ask_ai(question: str) -> str:
    try:
        url = f"https://generativelanguage.googleapis.com/v1/models/{MODEL_NAME}:generateContent?key={GEMINI_API_KEY}"
        headers = {"Content-Type": "application/json"}
        data = {"contents": [{"parts": [{"text": question}]}]}
        response = requests.post(url, headers=headers, json=data, timeout=15)
        
        if response.status_code != 200:
            return f"⚠ Gemini API Error: {response.text}"
        
        result = response.json()
        candidates = result.get("candidates")
        if candidates and len(candidates) > 0:
            content = candidates[0].get("content")
            if content and len(content) > 0:
                parts = content[0].get("parts")
                if parts and len(parts) > 0:
                    return parts[0].get("text", "No text found.")
        return "⚠ No response generated."
    except requests.exceptions.Timeout:
        return "⚠ Request timed out. Try again."
    except Exception as e:
        return f"⚠ Error: {str(e)}"

# -----------------------
# Streamlit WebRTC Callback
# -----------------------
def audio_frame_callback(frame: av.AudioFrame):
    """
    This callback converts audio frame to WAV and performs speech recognition
    """
    wav = frame.to_ndarray()
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        # Convert to proper WAV format
        import soundfile as sf
        sf.write(f.name, wav.T, samplerate=frame.sample_rate)
        # Speech recognition
        r = sr.Recognizer()
        with sr.AudioFile(f.name) as source:
            audio = r.record(source)
            try:
                text = r.recognize_google(audio)
                st.session_state.last_text = text
            except sr.UnknownValueError:
                st.session_state.last_text = "⚠ Could not understand audio"
            except sr.RequestError as e:
                st.session_state.last_text = f"⚠ STT request failed; {e}"
    return frame

# -----------------------
# Start WebRTC Streamer
# -----------------------
webrtc_streamer(key="voice_input", audio_receiver_size=1024, audio_frame_callback=audio_frame_callback)

# -----------------------
# Display Recognized Text
# -----------------------
if 'last_text' not in st.session_state:
    st.session_state.last_text = ""

st.subheader("🗣 Recognized Text")
st.write(st.session_state.last_text)

# -----------------------
# Send to Gemini API Button
# -----------------------
if st.session_state.last_text:
    if st.button("Send to Gemini AI"):
        response = ask_ai(st.session_state.last_text)
        st.subheader("🤖 AI Response")
        st.write(response)
