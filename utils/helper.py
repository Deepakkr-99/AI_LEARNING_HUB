import requests
from streamlit_lottie import st_lottie

def load_lottie_url(url: str, height: int = 150):
    """
    Load a Lottie animation from a URL and display in Streamlit.
    """
    try:
        r = requests.get(url, timeout=5)
        r.raise_for_status()  # Raise exception for HTTP errors
        st_lottie(r.json(), height=height)
    except requests.exceptions.RequestException as e:
        print(f"⚠ Failed to load Lottie animation: {e}")
    except Exception as e:
        print(f"⚠ Unexpected error in load_lottie_url: {e}")
