import streamlit as st
from streamlit_webrtc import webrtc_streamer
import speech_recognition as sr
import requests

MODEL_NAME = "gemini-2.5-flash"
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

st.title("🎤 Voice to Gemini AI")

# Button to start recording
st.write("Click below and speak:")
if st.button("Start Voice Input"):
    st.session_state.recording = True

if 'recording' not in st.session_state:
    st.session_state.recording = False

if st.session_state.recording:
    st.write("🎙 Recording... speak now!")
    
    # Using WebRTC for live audio
    webrtc_streamer(key="speech-to-text")

    # Using SpeechRecognition (offline example)
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            st.write("You said:", text)

            # Send to Gemini API
            url = f"https://generativelanguage.googleapis.com/v1/models/{MODEL_NAME}:generateContent?key={GEMINI_API_KEY}"
            data = {"contents":[{"parts":[{"text": text}]}]}
            headers = {"Content-Type":"application/json"}
            response = requests.post(url, headers=headers, json=data, timeout=15)
            if response.status_code == 200:
                result = response.json()
                st.write("AI Response:", result["candidates"][0]["content"][0]["parts"][0]["text"])
            else:
                st.write("API Error:", response.text)
        except Exception as e:
            st.write("⚠ Could not recognize speech:", str(e))
