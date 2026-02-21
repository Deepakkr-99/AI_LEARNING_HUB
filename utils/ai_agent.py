import streamlit as st
import requests

MODEL_NAME = "gemini-2.5-flash"

# Secure API key from Streamlit secrets
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

def ask_ai(question):
    try:
        url = f"https://generativelanguage.googleapis.com/v1/models/{MODEL_NAME}:generateContent?key={GEMINI_API_KEY}"

        headers = {
            "Content-Type": "application/json"
        }

        data = {
            "contents": [
                {
                    "parts": [
                        {"text": question}
                    ]
                }
            ]
        }

        response = requests.post(url, headers=headers, json=data, timeout=15)

        if response.status_code != 200:
            return f"Gemini Error: {response.text}"

        result = response.json()

        # Safe extraction
        candidates = result.get("candidates")
        if candidates:
            return candidates[0]["content"]["parts"][0]["text"]

        return "No response generated."

    except requests.exceptions.Timeout:
        return "⚠ Request timed out. Try again."

    except Exception as e:
        return f"Error: {str(e)}"