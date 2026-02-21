from utils.firebase_config import database
import pandas as pd

# 🔹 Log Progress for a User
def log_progress(username: str, topic: str, score: int) -> bool:
    try:
        progress_ref = database.child("progress").child(username)
        progress_ref.push({
            "Topic": topic,
            "Score": score
        })
        return True
    except Exception as e:
        print(f"⚠ Error logging progress for {username}: {e}")
        return False


# 🔹 Get Progress for a User
def get_progress(username: str) -> pd.DataFrame:
    try:
        progress_ref = database.child("progress").child(username).get()

        if not progress_ref:
            return pd.DataFrame(columns=["Topic", "Score"])

        df = pd.DataFrame(list(progress_ref.values()))

        # Ensure columns exist
        if "Topic" not in df.columns:
            df["Topic"] = ""
        if "Score" not in df.columns:
            df["Score"] = 0

        return df

    except Exception as e:
        print(f"⚠ Error fetching progress for {username}: {e}")
        return pd.DataFrame(columns=["Topic", "Score"])
