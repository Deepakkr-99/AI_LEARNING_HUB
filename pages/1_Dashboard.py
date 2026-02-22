import streamlit as st
from utils.progress_manager import get_progress
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

# 🔐 Login check
if "username" not in st.session_state:
    st.warning("Please login first")
    st.stop()

username = st.session_state["username"]

st.title(f"👋 Welcome, {username}")

df = get_progress(username)

# ---------- Prediction Function ----------
def predict_next_score(df):
    if df.empty:
        return 0

    df = df.copy()
    df["Score"] = pd.to_numeric(df["Score"], errors="coerce").fillna(0)

    if len(df) < 2:
        return round(df["Score"].mean(), 2)

    last = df["Score"].iloc[-1]
    prev = df["Score"].iloc[-2]

    prediction = last + (last - prev)
    prediction = max(0, min(100, prediction))

    return round(prediction, 2)


# ---------- Performance Level ----------
def performance_level(avg):
    if avg >= 80:
        return "🏆 Expert Level"
    elif avg >= 60:
        return "🔥 Good Performer"
    elif avg >= 40:
        return "⚡ Average"
    else:
        return "🚀 Needs Improvement"


# ---------- No Data ----------
if df.empty:
    st.info("No progress yet! Take quizzes to start tracking.")
else:
    df["Score"] = pd.to_numeric(df["Score"], errors="coerce").fillna(0)

    avg_score = df["Score"].mean()
    best_score = df["Score"].max()
    total_tests = len(df)
    predicted = predict_next_score(df)
    level = performance_level(avg_score)

    # ---------- Metrics ----------
    col1, col2, col3 = st.columns(3)
    col1.metric("📈 Average Score", f"{round(avg_score,2)} / 100")
    col2.metric("🏆 Best Score", f"{best_score} / 100")
    col3.metric("📝 Total Tests Taken", total_tests)

    st.markdown("### 🤖 AI Performance Insight")
    st.success(f"Performance Level: {level}")
    st.info(f"🎯 Predicted Next Score: {predicted}")

    # ---------- Professional Graph ----------
    st.markdown("### 📊 Performance Trend")

    fig = px.line(
        df,
        x="Topic",
        y="Score",
        markers=True,
        template="plotly_dark",
        title="Your Performance Trend"
    )

    fig.update_layout(yaxis_range=[0, 100])

    st.plotly_chart(fig, use_container_width=True)
