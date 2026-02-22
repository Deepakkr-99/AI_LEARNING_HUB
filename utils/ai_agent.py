import requests
import streamlit as st
import speech_recognition as sr

MODEL_NAME = "gemini-2.5-flash"
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

def ask_ai(question: str) -> str:
    """Send question to Gemini API and get AI response"""
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

def listen_and_ask() -> str:
    """Record voice, convert to text, send to AI, return AI response"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙 Listening... Please speak clearly.")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        st.success(f"You said: {text}")
        ai_response = ask_ai(text)
        return ai_response
    except Exception as e:
        return f"⚠ Error: {str(e)}"
