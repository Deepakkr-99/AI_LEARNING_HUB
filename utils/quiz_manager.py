from utils.firebase_config import database

def load_quizzes() -> list:
    """
    Load all quizzes from Firebase excluding users/progress/results.
    """
    try:
        data = database.get()
        if not data:
            return []
        quizzes = [{"topic":k,"questions":v.get("questions",[])}
                    for k,v in data.items() if k not in ["users","progress","results"]]
        return quizzes
    except Exception as e:
        print(f"⚠ Error loading quizzes: {e}")
        return []

def submit_quiz(username: str, topic: str, score: int) -> bool:
    """
    Submit user's quiz score to Firebase under results/username
    """
    try:
        database.child(f"results/{username}").push({"topic":topic,"score":score})
        return True
    except Exception as e:
        print(f"⚠ Error submitting quiz: {e}")
        return False
