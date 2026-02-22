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


if df.empty:
    st.info("No progress yet!")
else:
    df["Score"] = pd.to_numeric(df["Score"], errors="coerce").fillna(0)

    predicted = predict_next_score(df)

    # ---------- Professional Bar Chart ----------
    st.markdown("### 📊 Topic Performance")

    fig = px.bar(
        df,
        x="Topic",
        y="Score",
        text="Score",
        template="plotly_dark",
        title="Scores by Topic"
    )

    fig.update_traces(textposition="outside")
    fig.update_layout(yaxis_range=[0, 100])

    st.plotly_chart(fig, use_container_width=True)

    # ---------- AI Prediction Section ----------
    st.markdown("### 🔮 AI Prediction")
    st.info(f"Based on your performance trend, your next expected score is: {predicted}")
