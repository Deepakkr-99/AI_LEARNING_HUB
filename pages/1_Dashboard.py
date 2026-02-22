import streamlit as st
from utils.progress_manager import get_progress
from utils.ai_agent import predict_next_score, get_performance_level, get_weak_topic, get_strong_topic
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

if 'username' not in st.session_state:
    st.warning("Please login first")
    st.stop()

username = st.session_state['username']

st.markdown(f"## 👋 Welcome, {username}")

df = get_progress(username)

if df.empty:
    st.info("No progress yet! Take quizzes to start tracking.")
else:
    df["Score"] = pd.to_numeric(df["Score"], errors='coerce').fillna(0)

    avg_score = df["Score"].mean()
    best_score = df["Score"].max()
    total_tests = len(df)
    predicted_score = predict_next_score(df)
    performance = get_performance_level(avg_score)
    weak_topic = get_weak_topic(df)
    strong_topic = get_strong_topic(df)

    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📈 Average Score", round(avg_score, 2))
    col2.metric("🏆 Best Score", best_score)
    col3.metric("📝 Total Tests", total_tests)
    col4.metric("🤖 Predicted Next Score", predicted_score)

    st.markdown(f"### 🎖 Performance Level: {performance}")
    st.markdown(f"🔥 Strong Topic: **{strong_topic}**")
    st.markdown(f"⚠ Weak Topic: **{weak_topic}**")

    # Trend Chart
    fig = px.line(
        df,
        x="Timestamp",
        y="Score",
        markers=True,
        template="plotly_dark",
        title="📊 Performance Trend Over Time"
    )

    st.plotly_chart(fig, use_container_width=True)
