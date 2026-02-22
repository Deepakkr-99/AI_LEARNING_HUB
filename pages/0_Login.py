import streamlit as st
from utils.auth_manager import login_user, register_user

st.set_page_config(page_title="Login - NeuroSpark AI", page_icon="🔑", layout="centered")
st.markdown("## 🔑 Login or Register", unsafe_allow_html=True)

tab = st.radio("Select Mode", ["Login", "Register"], horizontal=True)
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Submit"):
    if tab == "Register":
        success, msg = register_user(username, password)
    else:
        success, msg = login_user(username, password)
        if success:
            st.session_state['username'] = username

    if success:
        st.success(msg)
        if tab == "Login":
            st.experimental_rerun()
    else:
        st.error(msg)
