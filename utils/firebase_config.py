import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

firebase_dict = st.secrets["firebase"]
database_url = st.secrets["FIREBASE_DATABASE_URL"]

if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_dict)
    firebase_admin.initialize_app(cred, {"databaseURL": database_url})

database = db.reference()
