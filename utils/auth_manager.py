from utils.firebase_config import database
import hashlib


# 🔐 Password Hash
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# 📝 Register User
def register_user(username, password):
    if not username or not password:
        return False, "Username and password required"

    username = username.strip()

    users_ref = database.child("users")
    user_data = users_ref.child(username).get()

    # Firebase Admin SDK returns dict directly
    if user_data:
        return False, "Username already exists"

    users_ref.child(username).set({
        "password": hash_password(password)
    })

    return True, "User registered successfully"


# 🔑 Login User
def login_user(username, password):
    if not username or not password:
        return False, "Enter username and password"

    username = username.strip()

    users_ref = database.child("users")
    user_data = users_ref.child(username).get()

    if user_data and user_data.get("password") == hash_password(password):
        return True, "Login successful"

    return False, "Invalid username or password"