import streamlit as st

st.set_page_config(
    page_title="Login - NeuroSpark AI",
    page_icon="🔑",
    layout="centered"
)

st.title("🔑 Login Page")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if username and password:
        st.success(f"Welcome {username} ✅")
    else:
        st.error("Please enter username and password ❌")
