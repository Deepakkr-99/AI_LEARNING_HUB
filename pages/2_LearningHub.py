import streamlit as st

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Learning Hub", page_icon="📘")

# ---------- LOGIN CHECK ----------
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("⚠ Please login first.")
    st.switch_page("pages/0_Login.py")
    st.stop()

# ---------- TITLE ----------
st.title("📘 AI Learning Hub")
st.write("Ask anything and grow smarter with AI 🚀")

# ---------- LOGOUT BUTTON ----------
if st.button("🚪 Logout"):
    st.session_state.clear()
    st.switch_page("pages/0_Login.py")
    st.stop()

# ---------- LOAD GEMINI ----------
try:
    import google.generativeai as genai
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception:
    st.error("❌ Gemini library install nahi hai ya API key missing hai.")
    st.stop()

# ---------- MODEL LOAD (Gemini 2.5 Flash) ----------
model = genai.GenerativeModel("gemini-2.5-flash")

# ---------- USER INPUT ----------
question = st.text_area("💬 Ask your AI Mentor:")

# ---------- AI RESPONSE ----------
if st.button("🚀 Ask AI"):
    if question.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.spinner("AI is thinking... 🤖"):
            try:
                response = model.generate_content(question)
                st.success("Here is your answer:")
                st.write(response.text)
            except Exception:
                st.error("❌ Error while generating response.")
