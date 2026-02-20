import requests
from streamlit_lottie import st_lottie

def load_lottie_url(url, height=150):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    st_lottie(r.json(), height=height)
