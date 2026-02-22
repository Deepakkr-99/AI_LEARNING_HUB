import streamlit as st

st.set_page_config(page_title="Learning Hub", page_icon="📘")

# 🔐 LOGIN PROTECTION (VERY IMPORTANT)
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("⚠ Please login first to access Learning Hub.")
    st.stop()   # ⛔ Yahi line page ko yahin rok degi

# ===============================
# ✅ USER LOGGED IN → PAGE OPEN
# ===============================

st.title("📘 AI Learning Hub")
st.success(f"Welcome {st.session_state['username']} 👋")

# 🔐 Gemini Setup
try:
    import google.generativeai as genai
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception:
    st.error("❌ Gemini library install nahi hai ya API key missing hai")
    st.stop()

model = genai.GenerativeModel("gemini-2.5-flash")

question = st.text_area("Ask your AI Mentor:")

if st.button("🚀 Ask AI"):
    if question.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.spinner("AI is thinking..."):
            response = model.generate_content(question)
            st.write(response.text)

# 🔓 Logout Button
if st.button("🚪 Logout"):
    st.session_state["logged_in"] = False
    st.session_state["username"] = None
    st.switch_page("pages/0_Login.py")
