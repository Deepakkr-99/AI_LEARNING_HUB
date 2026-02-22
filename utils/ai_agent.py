import streamlit as st
import requests
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, WebRtcMode
import numpy as np
import av
import speech_recognition as sr

MODEL_NAME = "gemini-2.5-flash"
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

def ask_ai(question: str) -> str:
    """Send question to Gemini API and get AI response."""
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


# ----------------- VOICE INPUT -----------------
st.title("🎤 Gemini AI Voice Assistant")

st.write("Press 'Start Mic' to speak your question:")

# Simple audio capture using streamlit_webrtc
class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.buffer = []

    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        # Convert audio to numpy array
        audio = frame.to_ndarray()
        self.buffer.append(audio)
        return frame

ctx = webrtc_streamer(
    key="voice",
    mode=WebRtcMode.SENDONLY,
    audio_processor_factory=AudioProcessor,
    media_stream_constraints={"audio": True, "video": False},
    async_processing=True
)

if ctx.state.playing:
    st.write("Listening... speak now.")
else:
    if ctx.audio_processor and ctx.audio_processor.buffer:
        # Combine all captured audio chunks
        audio_data = np.concatenate(ctx.audio_processor.buffer, axis=1)
        # Save to temporary WAV file
        import tempfile
        import soundfile as sf

        tmp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        sf.write(tmp_file.name, audio_data.T, 48000)  # transpose for soundfile

        # Use SpeechRecognition to convert to text
        recognizer = sr.Recognizer()
        with sr.AudioFile(tmp_file.name) as source:
            audio = recognizer.record(source)
            try:
                question_text = recognizer.recognize_google(audio)
                st.write(f"🗣 You said: {question_text}")
                # Send to Gemini AI
                answer = ask_ai(question_text)
                st.write(f"💡 AI says: {answer}")
            except sr.UnknownValueError:
                st.write("⚠ Could not understand audio")
            except sr.RequestError as e:
                st.write(f"⚠ Speech recognition error: {e}")
