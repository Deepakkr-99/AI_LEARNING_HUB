import pandas as pd
import os

PROGRESS_FILE = "data/progress.csv"

def log_progress(username, topic, score):
    if not os.path.exists(PROGRESS_FILE):
        df = pd.DataFrame(columns=["Username","Topic","Score"])
    else:
        df = pd.read_csv(PROGRESS_FILE)
    df = pd.concat([df, pd.DataFrame([[username, topic, score]], columns=df.columns)], ignore_index=True)
    df.to_csv(PROGRESS_FILE, index=False)

def get_progress(username):
    if not os.path.exists(PROGRESS_FILE):
        return pd.DataFrame()
    df = pd.read_csv(PROGRESS_FILE)
    return df[df['Username'] == username]
