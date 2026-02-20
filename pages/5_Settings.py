import streamlit as st
from utils.auth_manager import load_users, save_users, hash_password
import streamlit.components.v1 as components

st.set_page_config(page_title="Profile Settings", page_icon="⚙️", layout="centered")

# --------- PREMIUM CSS ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.main {
    background: linear-gradient(135deg, #141e30, #243b55);
}

.profile-card {
    background: rgba(255,255,255,0.08);
    padding: 30px;
    border-radius: 20px;
    backdrop-filter: blur(15px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    margin-bottom: 20px;
    animation: fadeIn 1s ease-in-out;
}

@keyframes fadeIn {
    from {opacity:0; transform: translateY(20px);}
    to {opacity:1; transform: translateY(0);}
}

.stButton>button {
    background: linear-gradient(90deg,#00c6ff,#0072ff);
    color:white;
    border-radius: 10px;
    font-weight:600;
    padding:8px 20px;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.05);
}
</style>
""", unsafe_allow_html=True)

# --------- LOGIN CHECK ----------
if 'username' not in st.session_state:
    st.warning("Please login first")
    st.stop()

username = st.session_state['username']
users = load_users()

# --------- PROFILE HEADER ----------
st.markdown(f"""
<div class="profile-card">
    <h2 style="color:white;">👤 Profile Settings</h2>
    <p style="color:#e0e0e0;">Logged in as: <b>{username}</b></p>
</div>
""", unsafe_allow_html=True)

# --------- CHANGE PASSWORD ----------
st.markdown("""
<div class="profile-card">
    <h4 style="color:white;">🔐 Change Password</h4>
</div>
""", unsafe_allow_html=True)

old_pass = st.text_input("Old Password", type="password")
new_pass = st.text_input("New Password", type="password")

# Password Strength Indicator
def password_strength(p):
    if len(p) < 6:
        return "Weak 🔴"
    elif len(p) < 10:
        return "Medium 🟡"
    else:
        return "Strong 🟢"

if new_pass:
    st.info(f"Password Strength: {password_strength(new_pass)}")

if st.button("Update Password"):
    if old_pass.strip() == "" or new_pass.strip() == "":
        st.error("Please fill both fields")
    elif users.get(username) == hash_password(old_pass):
        users[username] = hash_password(new_pass)
        save_users(users)
        st.success("✅ Password updated successfully!")
    else:
        st.error("❌ Old password is incorrect")

# --------- LOGOUT ----------
st.markdown("---")

if st.button("🚪 Logout"):
    del st.session_state['username']
    st.success("Logged out successfully!")
    st.switch_page("app.py")