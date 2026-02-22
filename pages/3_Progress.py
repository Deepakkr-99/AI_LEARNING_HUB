import streamlit as st
from utils.progress_manager import get_progress
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Progress", page_icon="📈", layout="wide")

if "username" not in st.session_state:
    st.warning("Please login first")
    st.stop()

username = st.session_state["username"]
st.title("📈 Detailed Progress Report")

df = get_progress(username)

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


if df.empty:
    st.info("No progress yet!")
else:
    df["Score"] = pd.to_numeric(df["Score"], errors="coerce").fillna(0)

    predicted = predict_next_score(df)

    # Topic Average Chart
    topic_avg = df.groupby("Topic")["Score"].mean().reset_index()

    st.markdown("### 📊 Topic-wise Average Performance")

    fig = px.bar(
        topic_avg,
        x="Topic",
        y="Score",
        text="Score",
        template="plotly_dark"
    )

    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig.update_layout(yaxis_range=[0, 100])

    st.plotly_chart(fig, use_container_width=True)

    # Score Distribution
    st.markdown("### 📈 Score Distribution")

    fig2 = px.histogram(
        df,
        x="Score",
        nbins=10,
        template="plotly_dark"
    )

    st.plotly_chart(fig2, use_container_width=True)

    # AI Prediction
    st.markdown("### 🔮 AI Prediction")
    st.success(f"Predicted Next Score: {predicted}")
