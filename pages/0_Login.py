import streamlit as st
from utils.auth_manager import login_user, register_user

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Login - NeuroSpark AI", page_icon="🔑", layout="centered")
st.markdown("## 🔑 Login or Register", unsafe_allow_html=True)

# ---------- INITIALIZE SESSION STATE ----------
if "username" not in st.session_state:
    st.session_state["username"] = None
if "tab" not in st.session_state:
    st.session_state["tab"] = "Login"

# ---------- SELECT MODE ----------
tab = st.radio("Select Mode", ["Login", "Register"], index=0 if st.session_state["tab"]=="Login" else 1, horizontal=True)
st.session_state["tab"] = tab  # remember selected tab

# ---------- INPUTS ----------
username_input = st.text_input("Username")
password_input = st.text_input("Password", type="password")

# ---------- SUBMIT BUTTON ----------
if st.button("Submit"):
    if tab == "Register":
        success, msg = register_user(username_input, password_input)
        if success:
            st.success(msg + " You can now login.")
        else:
            st.error(msg)
    else:  # Login
        success, msg = login_user(username_input, password_input)
        if success:
            st.session_state["username"] = username_input
            st.success(f"{msg} Welcome, {username_input}!")
        else:
            st.error(msg)

# ---------- SHOW APP OR LOGIN ----------
if st.session_state["username"]:
    st.write(f"✅ Logged in as **{st.session_state['username']}**")
    st.write("You can now access the app content here.")
