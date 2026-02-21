from utils.firebase_config import database
import hashlib

# 🔐 Password Hash
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


# 📝 Register User
def register_user(username: str, password: str) -> tuple[bool, str]:
    try:
        if not username or not password:
            return False, "Username and password required"

        username = username.strip()
        users_ref = database.child("users")
        user_data = users_ref.child(username).get()

        if user_data:
            return False, "Username already exists"

        users_ref.child(username).set({
            "password": hash_password(password)
        })
        return True, "User registered successfully"

    except Exception as e:
        return False, f"Error registering user: {e}"


# 🔑 Login User
def login_user(username: str, password: str) -> tuple[bool, str]:
    try:
        if not username or not password:
            return False, "Enter username and password"

        username = username.strip()
        users_ref = database.child("users")
        user_data = users_ref.child(username).get()

        if user_data and user_data.get("password") == hash_password(password):
            return True, "Login successful"

        return False, "Invalid username or password"

    except Exception as e:
        return False, f"Error logging in: {e}"
