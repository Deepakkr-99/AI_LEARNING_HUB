import streamlit as st
from utils.progress_manager import get_progress
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Progress - NeuroSpark AI", page_icon="📋", layout="wide")

if 'username' not in st.session_state:
    st.warning("Please login first")
    st.stop()

# ---------- Premium Styling ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');

html, body, [class*="css"]  {
    font-family: 'Montserrat', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0f2027, #2c5364);
}

.progress-card {
    background: rgba(255, 255, 255, 0.07);
    padding: 25px;
    border-radius: 20px;
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.2);
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='color:white;'>📋 Detailed Learning Progress</h1>", unsafe_allow_html=True)

df = get_progress(st.session_state['username'])

if df.empty:
    st.info("No progress recorded yet.")
else:
    df["Score"] = pd.to_numeric(df["Score"], errors="coerce")
    df = df.dropna(subset=["Score"])

    st.markdown("<div class='progress-card'>", unsafe_allow_html=True)

    st.dataframe(df, use_container_width=True)

    topic_avg = df.groupby("Topic")["Score"].mean().reset_index()

    fig = px.bar(
        topic_avg,
        x="Topic",
        y="Score",
        color="Score",
        template="plotly_dark",
        title="📊 Topic-wise Average Performance"
    )
    st.plotly_chart(fig, use_container_width=True)

    weak_topics = topic_avg[topic_avg["Score"] < 50]

    st.subheader("⚠ Weak Topics")
    if weak_topics.empty:
        st.success("🎉 No weak areas detected. Keep going!")
    else:
        st.warning("Focus more on these topics:")
        st.write(weak_topics)

    st.markdown("</div>", unsafe_allow_html=True)