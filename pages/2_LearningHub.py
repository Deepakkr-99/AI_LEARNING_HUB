import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI Learning Hub", page_icon="📘", layout="wide")

# 🔐 Login Check
if "username" not in st.session_state:
    st.warning("Please login first to use AI Mentor")
    st.stop()

username = st.session_state["username"]

st.title("📘 AI Learning Hub")
st.markdown(f"### 👋 Welcome {username}, Ask your AI Mentor anything!")

# 🔐 Load Gemini API
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception:
    st.error("❌ Gemini API Key missing or invalid")
    st.stop()

model = genai.GenerativeModel("gemini-2.5-flash")

# ---------------- Input Section ----------------
question = st.text_area("💬 Ask your AI Mentor:")

if st.button("🚀 Ask AI"):
    if question.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.spinner("🤖 AI is thinking..."):
            try:
                response = model.generate_content(question)

                st.markdown("## 🤖 AI Mentor Response")
                st.success("Here is your answer:")
                st.write(response.text)

            except Exception:
                st.error("❌ Error while generating response")
