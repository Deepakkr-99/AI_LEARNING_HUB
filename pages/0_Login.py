import hashlib

# 🔐 Password Hash Function
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# 🆕 Register User
def register_user(username, password):
    ref = db.reference("users")
    users = ref.get()

    if users and username in users:
        return False, "Username already exists"

    ref.child(username).set({
        "password": hash_password(password)
    })
    return True, "User registered successfully"

# 🔑 Login User
def login_user(username, password):
    ref = db.reference("users")
    user = ref.child(username).get()

    if not user:
        return False, "User does not exist"

    if user["password"] == hash_password(password):
        return True, "Login successful"
    else:
        return False, "Incorrect password"
