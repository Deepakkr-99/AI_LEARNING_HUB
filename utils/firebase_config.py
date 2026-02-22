import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import json

# -------------------------
# Get Firebase config from secrets
# -------------------------
firebase_json_str = st.secrets["firebase"]  # string from secrets
database_url = st.secrets["FIREBASE_DATABASE_URL"]

# Convert string to dict
firebase_dict = json.loads(firebase_json_str)

# Initialize Firebase once
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_dict)  # now it's a dict
    firebase_admin.initialize_app(cred, {"databaseURL": database_url})

# Database reference
database = db.reference()
