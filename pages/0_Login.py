
import streamlit as st
from utils.auth_manager import login_user, register_user

# ---------- Redirect from Landing ----------
if st.session_state.get("goto_login"):
    st.session_state.pop("goto_login")  # clear the flag

# ---------- Page Config ----------
st.set_page_config(
    page_title="Login - NeuroSpark AI",
    page_icon="🔑",
    layout="centered"
)

st.markdown("## 🔑 Login or Register", unsafe_allow_html=True)

# ---------- Initialize Session ----------
if "username" not in st.session_state:
    st.session_state["username"] = None

# ---------- Tab & Inputs ----------
tab = st.radio("Select Mode", ["Login", "Register"], horizontal=True)
username = st.text_input("Username")
password = st.text_input("Password", type="password")

# ---------- Submit Button ----------
if st.button("Submit"):
    if tab == "Register":
        success, msg = register_user(username, password)
        if success:
            st.success(msg + " You can now login.")
        else:
            st.error(msg)
    else:
        success, msg = login_user(username, password)
        if success:
            st.session_state["username"] = username
            st.success(f"{msg} Welcome, {username}!")
        else:
            st.error(msg)

# ---------- Logged-in Content ----------
if st.session_state.get("username"):
    st.write(f"✅ Logged in as **{st.session_state['username']}**")
    st.write("You can now access the app content here...")
