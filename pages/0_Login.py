import streamlit as st
from utils.auth_manager import login_user, register_user

# ---------- Page Config ----------
st.set_page_config(
    page_title="Login - NeuroSpark AI",
    page_icon="🔑",
    layout="centered"
)

# ---------- Custom CSS ----------
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg, #1f1c2c, #928dab);
}
.card {
    background: rgba(255,255,255,0.05);
    padding: 40px;
    border-radius: 20px;
    box-shadow: 0 0 30px rgba(0,0,0,0.4);
}
.big-title {
    text-align:center;
    font-size:32px;
    font-weight:700;
    margin-bottom:10px;
}
.subtitle {
    text-align:center;
    font-size:14px;
    color: #cccccc;
    margin-bottom:30px;
}
.stButton>button {
    width:100%;
    border-radius:12px;
    height:45px;
    font-weight:600;
    font-size:16px;
    background: linear-gradient(90deg,#ff512f,#dd2476);
    color:white;
    border:none;
}
.stButton>button:hover {
    background: linear-gradient(90deg,#dd2476,#ff512f);
}
</style>
""", unsafe_allow_html=True)

# ---------- Initialize Session ----------
if "username" not in st.session_state:
    st.session_state["username"] = None

# ---------- UI Layout ----------
st.markdown('<div class="card">', unsafe_allow_html=True)

st.markdown('<div class="big-title">🧠 NeuroSpark AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Smart Learning. AI Powered Growth.</div>', unsafe_allow_html=True)

tab = st.radio("Select Mode", ["Login", "Register"], horizontal=True)

username = st.text_input("👤 Username")
password = st.text_input("🔒 Password", type="password")

if st.button("🚀 Continue"):
    if not username or not password:
        st.warning("Please fill all fields")
    else:
        if tab == "Register":
            success, msg = register_user(username, password)
            if success:
                st.success("✅ " + msg + " You can now login.")
            else:
                st.error(msg)
        else:
            success, msg = login_user(username, password)
            if success:
                st.session_state["username"] = username
                st.success(f"🎉 {msg} Welcome, {username}!")
                st.rerun()
            else:
                st.error(msg)

# ---------- Logged-in Message ----------
if st.session_state.get("username"):
    st.success(f"✅ Logged in as {st.session_state['username']}")
    st.info("Use sidebar to navigate to Dashboard, Learning Hub, and more.")

st.markdown('</div>', unsafe_allow_html=True)
