import streamlit as st
from utils.progress_manager import get_progress
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

if 'username' not in st.session_state:
    st.warning("Please login first")
    st.stop()

username = st.session_state['username']

st.markdown(f"<h1 style='color:white;'>👋 Welcome, {username}</h1>", unsafe_allow_html=True)

df = get_progress(username)

if df.empty:
    st.info("No progress yet! Take quizzes to start tracking.")
else:
    df["Score"] = pd.to_numeric(df["Score"], errors='coerce').fillna(0)
    avg_score = df["Score"].mean()
    best_score = df["Score"].max()
    total_tests = len(df)

    col1, col2, col3 = st.columns(3)
    col1.metric("📈 Average Score", round(avg_score,2))
    col2.metric("🏆 Best Score", best_score)
    col3.metric("📝 Total Tests", total_tests)

    fig = px.line(df, x="Topic", y="Score", markers=True, template="plotly_dark", title="Performance Trend")
    st.plotly_chart(fig, use_container_width=True)
