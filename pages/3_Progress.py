import streamlit as st
from utils.progress_manager import get_progress
from utils.ai_agent import get_weak_topic, get_strong_topic
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Progress", page_icon="📈", layout="wide")

if 'username' not in st.session_state:
    st.warning("Please login first")
    st.stop()

username = st.session_state['username']
df = get_progress(username)

if df.empty:
    st.info("No progress yet!")
else:
    df["Score"] = pd.to_numeric(df["Score"], errors='coerce').fillna(0)

    # Topic wise average
    topic_avg = df.groupby("Topic")["Score"].mean().reset_index()

    fig1 = px.bar(
        topic_avg,
        x="Topic",
        y="Score",
        template="plotly_dark",
        title="📊 Topic Wise Average Score"
    )

    st.plotly_chart(fig1, use_container_width=True)

    # Improvement Chart
    fig2 = px.line(
        df,
        x="Timestamp",
        y="Score",
        markers=True,
        template="plotly_dark",
        title="📈 Score Improvement Over Time"
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.success(f"🔥 Strong Topic: {get_strong_topic(df)}")
    st.warning(f"⚠ Weak Topic: {get_weak_topic(df)}")
