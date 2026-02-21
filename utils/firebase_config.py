import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

# Get Firebase config from secrets
firebase_dict = st.secrets["firebase"]
database_url = st.secrets["FIREBASE_DATABASE_URL"]
gemini_key = st.secrets["GEMINI_API_KEY"]

# Initialize Firebase once
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_dict)
    firebase_admin.initialize_app(cred, {"databaseURL": database_url})

# Database reference
database = db.reference()
