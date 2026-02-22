import streamlit as st
from utils.progress_manager import get_progress
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
    fig = px.bar(df, x="Topic", y="Score", template="plotly_dark", title="Your Progress")
    st.plotly_chart(fig, use_container_width=True)
