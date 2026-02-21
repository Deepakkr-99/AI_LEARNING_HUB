import pandas as pd
from firebase_admin import db

# 🔹 Log Progress for a User
def log_progress(username, topic, score):
    try:
        ref = db.reference(f"progress/{username}")
        ref.push({
            "Topic": topic,
            "Score": score
        })
        return True, "Progress logged successfully"
    except Exception as e:
        return False, f"Error logging progress: {e}"

# 🔹 Get Progress for a User
def get_progress(username):
    try:
        ref = db.reference(f"progress/{username}")
        data = ref.get()

        if not data:
            return pd.DataFrame(columns=["Topic", "Score"])

        # Convert Firebase data to DataFrame with proper columns
        df = pd.DataFrame(list(data.values()))
        # Ensure columns exist
        if "Topic" not in df.columns:
            df["Topic"] = ""
        if "Score" not in df.columns:
            df["Score"] = 0

        return df

    except Exception as e:
        print(f"Error fetching progress: {e}")
        return pd.DataFrame(columns=["Topic", "Score"])
