import streamlit as st
from firebase_admin import db
from utils.auth_manager import hash_password

st.set_page_config(page_title="Settings", page_icon="⚙️", layout="centered")

# ---------------- LOGIN CHECK ----------------
if "username" not in st.session_state:
    st.warning("Please login first")
    st.stop()

username = st.session_state["username"]

# ---------------- Custom Styling ----------------
st.markdown("""
<style>
.big-title {
    font-size:28px;
    font-weight:700;
    text-align:center;
}
.card {
    padding:25px;
    border-radius:15px;
    background-color:#1e1e1e;
    box-shadow:0 0 20px rgba(0,0,0,0.4);
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-title">⚙️ Account Settings</div>', unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center;'>Logged in as <b>{username}</b></p>", unsafe_allow_html=True)

st.markdown('<div class="card">', unsafe_allow_html=True)

# ---------------- PASSWORD UPDATE SECTION ----------------
st.subheader("🔐 Change Password")

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

if st.button("✅ Update Password"):
    ref = db.reference("users")
    user = ref.child(username).get()

    if not old_pass or not new_pass:
        st.warning("Please fill all fields")

    elif user and user["password"] == hash_password(old_pass):
        ref.child(username).update({
            "password": hash_password(new_pass)
        })
        st.success("🎉 Password updated successfully!")

    else:
        st.error("❌ Old password incorrect")

st.markdown("---")

# ---------------- LOGOUT SECTION ----------------
st.subheader("🚪 Logout")

if st.button("🔓 Logout"):
    st.session_state.clear()
    st.success("Logged out successfully!")
    st.switch_page("pages/0_Login.py")

st.markdown('</div>', unsafe_allow_html=True)
