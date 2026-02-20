import json, os
from utils.progress_manager import log_progress

QUIZ_FILE = "data/quizzes.json"

def load_quizzes():
    if not os.path.exists(QUIZ_FILE) or os.stat(QUIZ_FILE).st_size == 0:
        return []
    with open(QUIZ_FILE, "r") as f:
        return json.load(f)

def save_quizzes(quizzes):
    with open(QUIZ_FILE, "w") as f:
        json.dump(quizzes, f, indent=4)

def submit_quiz(username, topic, score):
    log_progress(username, topic, score)
