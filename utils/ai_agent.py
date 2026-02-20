import requests

# 🔐 Apni Gemini API key yahan paste karo
GEMINI_API_KEY = "OPENAI_AI_KEY"

# 🔥 Model from your list
MODEL_NAME = "gemini-2.5-flash"

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

        response = requests.post(url, headers=headers, json=data)

        if response.status_code != 200:
            return f"Gemini Error: {response.text}"

        result = response.json()

        # Safe extraction
        if "candidates" in result:
            return result["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"Unexpected response: {result}"

    except Exception as e:

        return f"Error: {str(e)}"
