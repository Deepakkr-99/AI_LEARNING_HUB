import streamlit as st
from utils.quiz_manager import load_quizzes, submit_quiz

st.set_page_config(page_title="Quiz Zone", page_icon="🧠", layout="wide")

if 'username' not in st.session_state:
    st.warning("Login first")
    st.stop()

username = st.session_state['username']
quizzes = load_quizzes()
topics = [q['topic'] for q in quizzes]

st.markdown("<h1 style='color:white;'>📝 Quiz Zone</h1>", unsafe_allow_html=True)
topic = st.selectbox("Select Topic", topics)
questions = next((q['questions'] for q in quizzes if q['topic']==topic), [])

answers = [None]*len(questions)
with st.form("quiz_form"):
    for i,q in enumerate(questions):
        st.markdown(f"### Q{i+1}. {q['question']}")
        answers[i] = st.radio("Select answer:", q['options'], key=f"q{i}")
    submitted = st.form_submit_button("🚀 Submit Quiz")

if submitted:
    score = sum(1 for i,q in enumerate(questions) if answers[i]==q['answer'])
    submit_quiz(username, topic, score)
    st.success(f"You scored {score}/{len(questions)}")
