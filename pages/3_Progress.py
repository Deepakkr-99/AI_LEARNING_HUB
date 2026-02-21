import pandas as pd
from firebase_admin import db

def log_progress(username, topic, score):
    ref = db.reference(f"progress/{username}")
    ref.push({
        "Topic": topic,
        "Score": score
    })

def get_progress(username):
    ref = db.reference(f"progress/{username}")
    data = ref.get()

    if not data:
        return pd.DataFrame()

    df = pd.DataFrame(data.values())
    return df