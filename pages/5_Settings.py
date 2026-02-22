import streamlit as st
from firebase_admin import db
from utils.auth_manager import hash_password

st.set_page_config(page_title="Settings", page_icon="⚙️", layout="centered")

# ---------------- LOGIN CHECK ----------------
if "username" not in st.session_state:
    st.warning("Please login first")
    st.stop()

username = st.session_state["username"]

# ---------------- Modern CSS Styling ----------------
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg, #141e30, #243b55);
}

.title {
    font-size:34px;
    font-weight:800;
    text-align:center;
    margin-bottom:5px;
    color:white;
}

.subtitle {
    text-align:center;
    font-size:15px;
    color:#cccccc;
    margin-bottom:25px;
}

.card {
    background: rgba(255,255,255,0.05);
    padding:35px;
    border-radius:20px;
    box-shadow: 0 0 25px rgba(0,0,0,0.5);
}

/* Update Button */
div.stButton:nth-of-type(1) > button {
    width:100%;
    height:45px;
    border-radius:12px;
    font-size:16px;
    font-weight:600;
    background: linear-gradient(90deg,#00c6ff,#0072ff);
    color:white;
    border:none;
}
div.stButton:nth-of-type(1) > button:hover {
    background: linear-gradient(90deg,#0072ff,#00c6ff);
}

/* Logout Button */
div.stButton:nth-of-type(2) > button {
    width:100%;
    height:45px;
    border-radius:12px;
    font-size:16px;
    font-weight:600;
    background: linear-gradient(90deg,#ff512f,#dd2476);
    color:white;
    border:none;
}
div.stButton:nth-of-type(2) > button:hover {
    background: linear-gradient(90deg,#dd2476,#ff512f);
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<div class="title">⚙️ Account Settings</div>', unsafe_allow_html=True)
st.markdown(f'<div class="subtitle">Logged in as <b>{username}</b></div>', unsafe_allow_html=True)

st.markdown('<div class="card">', unsafe_allow_html=True)

# ---------------- PASSWORD UPDATE ----------------
st.markdown("### 🔐 Change Password")

old_pass = st.text_input("Old Password", type="password")
new_pass = st.text_input("New Password", type="password")

def password_strength(p):
    if len(p) < 6:
        return "Weak 🔴"
    elif len(p) < 10:
        return "Medium 🟡"
    else:
        return "Strong 🟢"

if new_pass:
    st.info(f"Password Strength: {password_strength(new_pass)}")

if st.button("🚀 Update Password"):
    ref = db.reference("users")
    user = ref.child(username).get()

    if not old_pass or not new_pass:
        st.warning("Please fill all fields")

    elif user and user["password"] == hash_password(old_pass):
        ref.child(username).update({
            "password": hash_password(new_pass)
        })
        st.success("🎉 Password updated successfully!")
        st.balloons()

    else:
        st.error("❌ Old password incorrect")

st.markdown("---")

# ---------------- LOGOUT SECTION ----------------
st.markdown("### 🚪 Secure Logout")

if st.button("🔓 Logout Now"):
    st.session_state.clear()
    st.success("Logged out successfully!")
    st.switch_page("pages/0_Login.py")

st.markdown('</div>', unsafe_allow_html=True)
