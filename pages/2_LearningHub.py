import streamlit as st

st.set_page_config(page_title="Learning Hub", page_icon="📘")

st.title("📘 AI Learning Hub")

# 🔐 Load API Key safely
try:
    import google.generativeai as genai
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("❌ Gemini library install nahi hai ya API key missing hai")
    st.stop()

# 🎯 Model Load
model = genai.GenerativeModel("gemini-1.5-flash")

# 💬 User Input
question = st.text_area("Ask your AI Mentor:")

if st.button("🚀 Ask AI"):
    if question.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.spinner("AI is thinking..."):
            try:
                response = model.generate_content(question)
                st.success("Here is your answer:")
                st.write(response.text)
            except Exception as e:
                st.error("❌ Error while generating response")
