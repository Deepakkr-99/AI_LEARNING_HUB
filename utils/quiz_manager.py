from utils.firebase_config import database
import pandas as pd

# ---------- Load Quizzes ----------
def load_quizzes():
    """
    Load all quiz topics from Firebase, excluding 'users' node.
    Returns a list of quizzes: [{"topic": str, "questions": [...]}]
    """
    try:
        data = database.get()
        if not data:
            return []

        # Filter out non-quiz keys (like 'users', 'progress', 'results')
        quizzes = [
            {"topic": k, "questions": v.get("questions", [])}
            for k, v in data.items()
            if k not in ["users", "progress", "results"]
        ]
        return quizzes

    except Exception as e:
        print(f"⚠ Error loading quizzes: {e}")
        return []


# ---------- Submit Quiz ----------
def submit_quiz(username: str, topic: str, score: int) -> bool:
    """
    Save user's quiz score in Firebase under 'results/{username}'.
    Returns True if saved successfully, False otherwise.
    """
    try:
        ref = database.child(f'results/{username}')
        ref.push({
            "topic": topic,
            "score": score
        })
        print(f"✅ Score saved for {username} - {topic}: {score}")
        return True

    except Exception as e:
        print(f"⚠ Error submitting quiz for {username}: {e}")
        return False
