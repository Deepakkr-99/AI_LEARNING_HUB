# pages/2_LearningHub.py
import streamlit as st
from utils.firebase_config import database
from utils.ai_agent import ask_gemini

st.set_page_config(page_title="Learning Hub", layout="wide")
st.title("📚 Learning Hub")

# Fetch lessons from Firebase (Admin SDK)
lessons = database.child("lessons").get()  # No .val() needed

if lessons:
    for lesson_id, lesson_data in lessons.items():
        with st.expander(lesson_data.get("title", f"Lesson {lesson_id}")):
            st.write(lesson_data.get("content", "No content available"))

            # AI Question input for this lesson
            user_question = st.text_input(
                f"Ask AI about {lesson_data.get('title')}:",
                key=f"question_{lesson_id}"
            )
            if st.button("Explain with AI", key=f"ai_{lesson_id}"):
                explanation = ask_gemini(user_question)
                st.info(explanation)
else:
    st.warning("No lessons found. Make sure your Firebase DB has a 'lessons' node.")
