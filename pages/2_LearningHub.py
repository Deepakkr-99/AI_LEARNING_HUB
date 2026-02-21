import streamlit as st
from utils.ai_agent import ask_ai
from utils.helper import load_lottie_url
import streamlit.components.v1 as components

st.set_page_config(page_title="AI Learning Hub", page_icon="📚", layout="wide")

# ---------- PREMIUM CSS ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.main {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}

.block-container {
    padding-top: 2rem;
}

.glass-card {
    background: rgba(255,255,255,0.08);
    padding: 30px;
    border-radius: 20px;
    backdrop-filter: blur(18px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.35);
    margin-bottom: 25px;
    animation: fadeIn 0.8s ease-in-out;
}

@keyframes fadeIn {
    from {opacity:0; transform: translateY(20px);}
    to {opacity:1; transform: translateY(0);}
}

.stTextArea textarea {
    border-radius: 15px !important;
    padding: 15px !important;
}

.stButton>button {
    background: linear-gradient(90deg,#00c6ff,#0072ff);
    color:white;
    border-radius: 12px;
    font-weight:600;
    padding:10px 25px;
    transition: 0.3s ease-in-out;
}

.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 20px #00c6ff;
}
</style>
""", unsafe_allow_html=True)

# ---------- LOGIN CHECK ----------
if 'username' not in st.session_state:
    st.warning("Please login first")
    st.stop()

# ---------- HEADER ----------
st.markdown(f"""
<div class="glass-card">
    <h1 style="color:white;">📚 AI Learning Hub</h1>
    <p style="color:#dcdcdc;">Welcome back, <b>{st.session_state['username']}</b> 👋</p>
    <p style="color:#b0c4de;">Ask anything and your AI Mentor will guide you instantly.</p>
</div>
""", unsafe_allow_html=True)

# ---------- ANIMATION ----------
load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_w51pcehl.json", height=160)

# ---------- VOICE INPUT WITH ON/OFF ----------
components.html("""
<div style="text-align:center;margin-bottom:15px;">

<button id="micBtn" onclick="startDictation()" 
style="
background: linear-gradient(90deg,#ff512f,#dd2476);
color:white;
border:none;
padding:12px 25px;
border-radius:30px;
font-weight:600;
cursor:pointer;
transition:0.3s;">
🎙 Start Voice Input
</button>

<p id="status" style="color:white;font-weight:600;margin-top:10px;"></p>

</div>

<script>

let recognition;
let isListening = false;

function startDictation() {

  if (!('webkitSpeechRecognition' in window)) {
      alert("Speech Recognition not supported in this browser");
      return;
  }

  if (!isListening) {

      recognition = new webkitSpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = "en-US";  // Change to "hi-IN" for Hindi

      recognition.start();
      isListening = true;

      document.getElementById("micBtn").innerHTML = "🔴 Listening...";
      document.getElementById("micBtn").style.boxShadow = "0 0 25px red";
      document.getElementById("status").innerHTML = "🎧 AI is Listening... Speak now";

      recognition.onresult = function(e) {
          const text = e.results[0][0].transcript;
          const textarea = window.parent.document.querySelector('textarea');
          if(textarea){
            textarea.value = text;
            textarea.dispatchEvent(new Event('input', { bubbles: true }));
          }
          stopListening();
      };

      recognition.onerror = function(e) {
          stopListening();
      };

      recognition.onend = function() {
          stopListening();
      };

  } else {
      stopListening();
  }
}

function stopListening() {
    if (recognition) recognition.stop();
    isListening = false;
    document.getElementById("micBtn").innerHTML = "🎙 Start Voice Input";
    document.getElementById("micBtn").style.boxShadow = "none";
    document.getElementById("status").innerHTML = "";
}

</script>
""", height=150)

# ---------- QUESTION AREA ----------
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

question = st.text_area("💬 Ask your AI Mentor:", height=120)

if st.button("🚀 Ask AI") and question.strip() != "":
    with st.spinner("🤖 AI is thinking..."):
        answer = ask_ai(question)
        st.markdown(f"""
        <div class="glass-card">
            <h4 style="color:white;">🤖 AI Mentor Response</h4>
            <p style="color:#e6e6e6;">{answer}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)