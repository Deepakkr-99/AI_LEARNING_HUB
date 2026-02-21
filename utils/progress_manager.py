from utils.firebase_config import database
import pandas as pd

def log_progress(username, topic, score):
    progress_ref = database.child("progress").child(username)

    progress_ref.push({
        "Topic": topic,
        "Score": score
    })

    return True


def get_progress(username):
    progress_ref = database.child("progress").child(username).get()

    if not progress_ref:
        return pd.DataFrame()

    df = pd.DataFrame(progress_ref.values())
    return df