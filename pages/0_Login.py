import streamlit as st
from utils.auth_manager import login_user, register_user

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Login - NeuroSpark AI",
    page_icon="🔑",
    layout="centered"
)

st.markdown("## 🔑 Login or Register")

# ---------- SESSION INIT ----------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "username" not in st.session_state:
    st.session_state["username"] = None

# ---------- IF ALREADY LOGGED IN ----------
if st.session_state["logged_in"]:
    st.success(f"✅ Already logged in as {st.session_state['username']}")
    if st.button("Go to Learning Hub"):
        st.switch_page("pages/2_LearningHub.py")
    st.stop()

# ---------- TAB SELECT ----------
tab = st.radio("Select Mode", ["Login", "Register"], horizontal=True)

username = st.text_input("Username")
password = st.text_input("Password", type="password")

# ---------- SUBMIT ----------
if st.button("Submit"):

    if username.strip() == "" or password.strip() == "":
        st.warning("Please enter username and password.")
        st.stop()

    if tab == "Register":
        success, msg = register_user(username, password)

        if success:
            st.success("✅ " + msg)
            st.info("Now login with your credentials.")
        else:
            st.error("❌ " + msg)

    else:  # LOGIN
        success, msg = login_user(username, password)

        if success:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username

            st.success(f"🎉 {msg} Welcome {username}!")
            st.switch_page("pages/2_LearningHub.py")

        else:
            st.error("❌ " + msg)
