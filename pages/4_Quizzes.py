import streamlit as st
from utils.quiz_manager import load_quizzes, submit_quiz

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Quiz Zone", page_icon="🧠", layout="wide")

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap');

html, body, [class*="css"]  {
    font-family: 'Poppins', sans-serif;
}

.main {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
}

h1 {
    text-align: center;
    font-weight: 700;
    animation: fadeIn 1.5s ease-in-out;
}

@keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
}

.stButton>button {
    background: linear-gradient(90deg,#ff8a00,#e52e71);
    color:white;
    border-radius:10px;
    font-weight:600;
    transition:0.3s;
}

.stButton>button:hover {
    transform: scale(1.05);
}
</style>
""", unsafe_allow_html=True)

# ---------- LOGIN CHECK ----------
if 'username' not in st.session_state:
    st.warning("Please login first")
    st.stop()

st.markdown("<h1>📝 Interactive Quiz Zone</h1>", unsafe_allow_html=True)

quizzes = load_quizzes()
topics = [q['topic'] for q in quizzes]

topic = st.selectbox("🎯 Select Topic:", topics)

for quiz in quizzes:
    if quiz['topic'] == topic:
        questions = quiz['questions']
        break

score = 0
user_answers = []

with st.container():
    for i, q in enumerate(questions):
        st.markdown(f"### Q{i+1}. {q['question']}")
        answer = st.radio("", q['options'], key=i)
        user_answers.append(answer)

if st.button("🚀 Submit Quiz"):
    score = sum([1 for i, q in enumerate(questions) if user_answers[i] == q['answer']])
    submit_quiz(st.session_state['username'], topic, score)
    st.success(f"🎉 You scored {score} out of {len(questions)}!")