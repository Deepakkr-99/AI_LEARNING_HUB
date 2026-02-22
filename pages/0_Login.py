import streamlit as st
from utils.auth_manager import login_user, register_user

st.set_page_config(page_title="Login - NeuroSpark AI", page_icon="🔑", layout="centered")
st.markdown("## 🔑 Login or Register", unsafe_allow_html=True)

# ---------- Mode Selection ----------
tab = st.radio("Select Mode", ["Login", "Register"], horizontal=True)

username = st.text_input("Username")
password = st.text_input("Password", type="password")

# ---------- Submit ----------
if st.button("Submit"):
    if not username or not password:
        st.warning("Enter both username and password")
    else:
        if tab == "Register":
            try:
                success, msg = register_user(username, password)
            except Exception as e:
                success = False
                msg = f"Registration Error: {e}"
        else:  # Login
            try:
                success, msg = login_user(username, password)
            except Exception as e:
                success = False
                msg = f"Login Error: {e}"

        if success:
            st.success(msg)
            if tab == "Login":
                st.session_state['username'] = username
                st.experimental_rerun()  # safe: session_state set
        else:
            st.error(msg)
