from utils.firebase_config import database
from utils.progress_manager import log_progress

def load_quizzes() -> list:
    try:
        data = database.get()

        if not data:
            return []

        quizzes = [
            {"topic": k, "questions": v.get("questions", [])}
            for k, v in data.items()
            if k not in ["users", "progress"]
        ]

        return quizzes

    except Exception as e:
        print("Error loading quizzes:", e)
        return []


def submit_quiz(username: str, topic: str, score: int) -> bool:
    try:
        log_progress(username, topic, score)
        return True
    except Exception as e:
        print("Error submitting quiz:", e)
        return False
