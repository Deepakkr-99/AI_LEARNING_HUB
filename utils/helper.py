import requests
from streamlit_lottie import st_lottie

def load_lottie_url(url, height=150):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            return
        st_lottie(r.json(), height=height)
    except Exception:
        return