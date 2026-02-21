import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import json

if not firebase_admin._apps:
    try:
        firebase_dict = json.loads(st.secrets["firebase"])
        cred = credentials.Certificate(firebase_dict)

        firebase_admin.initialize_app(
            cred,
            {
                "databaseURL": st.secrets["databaseURL"]
            }
        )

    except Exception as e:
        st.error("Firebase initialization failed")
        st.exception(e)

database = db.reference()