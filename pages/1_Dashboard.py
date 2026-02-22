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

# ------------------ AI Prediction ------------------
def predict_next_score(df):
    if df.empty:
        return 0

    df = df.copy()
    df["Score"] = pd.to_numeric(df["Score"], errors="coerce").fillna(0)

    if len(df) < 3:
        return round(df["Score"].mean(), 2)

    recent_avg = df["Score"].tail(3).mean()
    overall_avg = df["Score"].mean()

    prediction = (recent_avg * 0.7) + (overall_avg * 0.3)
    return round(max(0, min(100, prediction)), 2)


# ------------------ Performance Level ------------------
def performance_level(avg):
    if avg >= 85:
        return "🏆 Master"
    elif avg >= 70:
        return "🔥 Advanced"
    elif avg >= 50:
        return "⚡ Intermediate"
    else:
        return "🚀 Beginner"


if df.empty:
    st.info("No progress yet! Take quizzes to start tracking.")
else:
    df["Score"] = pd.to_numeric(df["Score"], errors="coerce").fillna(0)

    avg_score = df["Score"].mean()
    best_score = df["Score"].max()
    total_tests = len(df)
    predicted = predict_next_score(df)
    level = performance_level(avg_score)

    improvement = 0
    if len(df) > 1:
        improvement = df["Score"].iloc[-1] - df["Score"].iloc[0]

    weakest_topic = df.loc[df["Score"].idxmin()]["Topic"]

    # ------------------ Metrics ------------------
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📈 Average", f"{round(avg_score,2)}")
    col2.metric("🏆 Best", f"{best_score}")
    col3.metric("📝 Tests", total_tests)
    col4.metric("📊 Improvement", f"{improvement}")

    # ------------------ AI Insight ------------------
    st.markdown("### 🤖 AI Performance Insight")

    st.success(f"Performance Level: {level}")
    st.info(f"🎯 Predicted Next Score: {predicted}")
    st.warning(f"📌 Weakest Topic: {weakest_topic}")

    # ------------------ Performance Graph ------------------
    st.markdown("### 📊 Performance Trend")

    fig = px.line(
        df,
        y="Score",
        markers=True,
        template="plotly_dark"
    )

    fig.update_layout(yaxis_range=[0, 100])
    st.plotly_chart(fig, use_container_width=True)
