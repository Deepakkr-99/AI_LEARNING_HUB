from utils.firebase_config import database
import pandas as pd

def log_progress(username: str, topic: str, score: int) -> bool:
    try:
        database.child("progress").child(username).push({
            "Topic": topic,
            "Score": score
        })
        return True
    except Exception as e:
        print("Error logging progress:", e)
        return False


def get_progress(username: str) -> pd.DataFrame:
    try:
        data = database.child("progress").child(username).get()

        if not data:
            return pd.DataFrame(columns=["Topic", "Score"])

        df = pd.DataFrame(list(data.values()))

        if "Topic" not in df.columns:
            df["Topic"] = ""

        if "Score" not in df.columns:
            df["Score"] = 0

        return df

    except Exception as e:
        print("Error fetching progress:", e)
        return pd.DataFrame(columns=["Topic", "Score"])
