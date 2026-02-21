import streamlit as st
from utils.progress_manager import get_progress
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Dashboard - NeuroSpark AI", page_icon="📊", layout="wide")

# 🔐 Login Check
if 'username' not in st.session_state:
    st.warning("Please login first")
    st.stop()

# 🎨 Styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

html, body, [class*="css"]  {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #141e30, #243b55);
}

.glass-card {
    background: rgba(255, 255, 255, 0.08);
    padding: 25px;
    border-radius: 20px;
    backdrop-filter: blur(12px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.2);
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

st.markdown(f"<h1 style='color:white;'>👋 Welcome, {st.session_state['username']}</h1>", unsafe_allow_html=True)
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

# 📊 Get Data from Firebase
df = get_progress(st.session_state['username'])

if df.empty:
    st.info("No progress yet! Take quizzes to start tracking.")
else:

    # 🔎 Safety Check
    if "Score" not in df.columns:
        st.error("Score data missing in database.")
        st.stop()

    df["Score"] = pd.to_numeric(df["Score"], errors="coerce")
    df = df.dropna(subset=["Score"])

    if df.empty:
        st.info("No valid score data found.")
        st.stop()

    avg_score = round(df["Score"].mean(), 2)
    best_score = df["Score"].max()
    total_tests = len(df)

    col1, col2, col3 = st.columns(3)
    col1.metric("📈 Average Score", avg_score)
    col2.metric("🏆 Best Score", best_score)
    col3.metric("📝 Total Tests", total_tests)

    fig = px.line(
        df,
        x="Topic",
        y="Score",
        markers=True,
        template="plotly_dark",
        title="📊 Performance Trend"
    )
    st.plotly_chart(fig, use_container_width=True)

    # 🤖 Simple AI Prediction
    if len(df) >= 2:
        improvement = df["Score"].iloc[-1] - df["Score"].iloc[0]
        predicted_score = avg_score + (improvement / len(df))
    else:
        predicted_score = avg_score

    predicted_score = max(0, min(100, predicted_score))

    st.subheader("🤖 AI Prediction")
    st.metric("📊 Predicted Next Score", round(predicted_score, 2))

st.markdown("</div>", unsafe_allow_html=True)