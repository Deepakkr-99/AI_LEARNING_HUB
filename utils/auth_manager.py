import json, hashlib, os

USER_FILE = "data/users.json"

def load_users():
    if not os.path.exists(USER_FILE) or os.stat(USER_FILE).st_size == 0:
        return {}
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    users = load_users()
    if username in users:
        return False, "Username already exists"
    users[username] = hash_password(password)
    save_users(users)
    return True, "User registered successfully"

def login_user(username, password):
    users = load_users()
    if username in users and users[username] == hash_password(password):
        return True
    return False
