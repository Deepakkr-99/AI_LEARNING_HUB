# firebase_config.py
import firebase_admin
from firebase_admin import credentials, db
import streamlit as st

# ✅ Directly get dict from secrets, no json.loads
firebase_dict = st.secrets["firebase"]

database_url = st.secrets["FIREBASE_DATABASE_URL"]

# Initialize Firebase only once
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_dict)
    firebase_admin.initialize_app(cred, {"databaseURL": database_url})

# Database reference
database = db.reference()
