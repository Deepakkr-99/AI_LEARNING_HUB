import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import json

# ---------- FIREBASE INITIALIZATION ----------
if not firebase_admin._apps:
    try:
        # Load Firebase service account from secrets
        firebase_dict = json.loads(st.secrets["firebase"])
        cred = credentials.Certificate(firebase_dict)

        # Initialize app with Realtime Database URL from secrets
        firebase_admin.initialize_app(
            cred,
            {
                "databaseURL": st.secrets.get("databaseURL", "")
            }
        )
        st.success("Firebase initialized successfully ✅")

    except Exception as e:
        st.error("Firebase initialization failed ❌")
        st.exception(e)

# ---------- DATABASE REFERENCE ----------
database = db.reference()
