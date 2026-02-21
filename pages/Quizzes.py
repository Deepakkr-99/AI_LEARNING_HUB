import streamlit as st
from utils.quiz_manager import load_quizzes, submit_quiz

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Quiz Zone", page_icon="🧠", layout="wide")

# ---------- LOGIN CHECK ----------
if 'username' not in st.session_state:
    st.warning("Please login first")
    st.stop()

username = st.session_state['username']

# ---------- LOAD QUIZZES ----------
quizzes = load_quizzes()

if not quizzes:
    st.error("No quizzes available.")
    st.stop()

topics = [q['topic'] for q in quizzes]

st.markdown("<h1 style='text-align:center;'>📝 Interactive Quiz Zone</h1>", unsafe_allow_html=True)

topic = st.selectbox("🎯 Select Topic:", topics)

# ---------- GET QUESTIONS ----------
questions = []
for quiz in quizzes:
    if quiz['topic'] == topic:
        questions = quiz.get('questions', [])
        break

if not questions:
    st.warning("No questions found for this topic.")
    st.stop()

# ---------- QUIZ FORM ----------
user_answers = [None] * len(questions)  # Initialize answers list

with st.form("quiz_form"):
    for i, q in enumerate(questions):
        st.markdown(f"### Q{i+1}. {q['question']}")
        user_answers[i] = st.radio(
            "Select your answer:",
            q['options'],
            key=f"q_{i}"
        )

    submitted = st.form_submit_button("🚀 Submit Quiz")

# ---------- SUBMIT LOGIC ----------
if submitted:
    score = sum(
        1 for i, q in enumerate(questions)
        if user_answers[i] == q['answer']
    )

    # Submit to Firebase / log progress
    submit_quiz(username, topic, score)

    st.success(f"🎉 You scored {score} out of {len(questions)}!")
