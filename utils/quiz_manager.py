import firebase_admin
from firebase_admin import credentials, db
import utils.firebase_config # Aapka purana connection logic

def load_quizzes():
    # Realtime Database se data lane ke liye
    ref = db.reference('/') 
    data = ref.get()
    
    # Sirf quizzes wale topics ko filter karein
    quizzes = {k: v for k, v in data.items() if k not in ['users']}
    return quizzes

def submit_quiz(username, topic, score):
    # Results ko "results" folder mein save karne ke liye
    ref = db.reference(f'results/{username}')
    ref.push({
        "topic": topic,
        "score": score
    })
    print("Score save ho gaya!")