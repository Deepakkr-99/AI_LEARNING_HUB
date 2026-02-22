import streamlit as st
from firebase_admin import db
from utils.auth_manager import hash_password

st.set_page_config(page_title="Settings", page_icon="⚙️", layout="centered")

if 'username' not in st.session_state:
    st.warning("Login first")
    st.stop()

username = st.session_state['username']
st.markdown(f"<h2 style='color:white;'>Profile Settings: {username}</h2>", unsafe_allow_html=True)

old_pass = st.text_input("Old Password", type="password")
new_pass = st.text_input("New Password", type="password")

def password_strength(p):
    if len(p)<6: return "Weak 🔴"
    elif len(p)<10: return "Medium 🟡"
    return "Strong 🟢"

if new_pass: st.info(f"Password Strength: {password_strength(new_pass)}")

if st.button("Update Password"):
    ref = db.reference("users")
    user = ref.child(username).get()
    if user and user["password"]==hash_password(old_pass):
        ref.child(username).update({"password": hash_password(new_pass)})
        st.success("Password updated!")
    else: st.error("Old password incorrect")
