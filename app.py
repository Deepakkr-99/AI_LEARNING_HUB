import streamlit as st

st.set_page_config(
    page_title="NeuroSpark AI",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 NeuroSpark AI")
st.write("Your Intelligent Learning Companion 🚀")

st.markdown("---")

if st.button("✨ Get Started"):
    st.switch_page("pages/1_Login.py")
