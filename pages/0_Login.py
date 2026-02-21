import streamlit as st
from firebase_admin import credentials, initialize_app, db
import hashlib

# ------------------- Firebase Setup ------------------- #
cred = credentials.Certificate("path/to/serviceAccountKey.json")  # Firebase service account
initialize_app(cred, {
    "databaseURL": "https://YOUR_PROJECT_ID.firebaseio.com/"
})

# ------------------- Utility Functions ------------------- #
def hash_password(password):
    """Hash the password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    ref = db.reference("users")
    users = ref.get()
    
    if users and username in users:
        return False, "Username already exists"
    
    ref.child(username).set({
        "password": hash_password(password)
    })
    return True, "User registered successfully"

def login_user(username, password):
    ref = db.reference("users")
    user = ref.child(username).get()
    
    if user and user["password"] == hash_password(password):
        return True
    return False

# ------------------- Streamlit UI ------------------- #
st.set_page_config(page_title="Professional Login System", page_icon="🔐", layout="centered")

st.markdown(
    """
    <h1 style='text-align: center; color: #4CAF50;'>🔐 Welcome to Secure Login System</h1>
    <p style='text-align: center; color: gray;'>Please login or register to continue</p>
    """, unsafe_allow_html=True
)

# Tabs for Login / Register
tab = st.tabs(["Login", "Register"])

# ------------------- LOGIN TAB ------------------- #
with tab[0]:
    st.subheader("Login")
    username_login = st.text_input("Username", key="login_user")
    password_login = st.text_input("Password", type="password", key="login_pass")
    
    if st.button("Login", key="login_btn"):
        if not username_login or not password_login:
            st.warning("⚠️ Please enter both username and password")
        elif login_user(username_login, password_login):
            st.success(f"✅ Welcome back, {username_login}!")
        else:
            st.error("❌ Invalid username or password")

# ------------------- REGISTER TAB ------------------- #
with tab[1]:
    st.subheader("Register")
    username_reg = st.text_input("Username", key="reg_user")
    password_reg = st.text_input("Password", type="password", key="reg_pass")
    confirm_pass = st.text_input("Confirm Password", type="password", key="reg_confirm")
    
    if st.button("Register", key="reg_btn"):
        if not username_reg or not password_reg or not confirm_pass:
            st.warning("⚠️ All fields are required")
        elif password_reg != confirm_pass:
            st.error("❌ Passwords do not match")
        else:
            success, message = register_user(username_reg, password_reg)
            if success:
                st.success(f"✅ {message}")
            else:
                st.error(f"❌ {message}")
