# utils/ai_agent.py
import streamlit as st
import requests
import json

# Load Gemini API key from Streamlit secrets
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

def ask_gemini(prompt: str) -> str:
    """
    Sends a prompt to Gemini AI and returns the response.
    """
    try:
        url = "https://api.gemini.ai/v1/chat"  # Replace with actual endpoint if different
        headers = {
            "Authorization": f"Bearer {GEMINI_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "gemini-2.5",  # your model version
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 300
        }

        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        result = response.json()

        # Extract AI response
        answer = result['choices'][0]['message']['content']
        return answer

    except Exception as e:
        return f"Error: {str(e)}"
