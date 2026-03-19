import streamlit as st
import random
import time
import base64
import json
from datetime import datetime
import streamlit.components.v1 as components

# --- PAGE CONFIG ---
st.set_page_config(page_title="Skyluxe Exclusive", page_icon="🏢", layout="centered")

# --- PREMIUM LUXURY CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;600&family=Cinzel:wght@400;600;700&family=Raleway:wght@300;400;500&display=swap');

    :root {
        --gold: #C9A84C;
        --gold-light: #E8C97A;
        --gold-dim: rgba(201,168,76,0.15);
        --gold-border: rgba(201,168,76,0.35);
        --dark: #0B0C0F;
        --dark-2: #13141A;
        --dark-3: #1C1E27;
        --text-muted: rgba(255,255,255,0.45);
    }

    html, body, .stApp {
        background-color: var(--dark) !important;
        font-family: 'Raleway', sans-serif;
        overflow: hidden; /* Prevent scrolling on mobile if possible */
    }

    .stApp {
        background-image: 
            radial-gradient(ellipse 80% 50% at 50% -10%, rgba(201,168,76,0.08) 0%, transparent 70%),
            repeating-linear-gradient(0deg, transparent, transparent 60px, rgba(201,168,76,0.015) 60px, rgba(201,168,76,0.015) 61px),
            repeating-linear-gradient(90deg, transparent, transparent 60px, rgba(201,168,76,0.015) 60px, rgba(201,168,76,0.015) 61px) !important;
    }

    /* Tighten up padding for mobile */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        max-width: 500px !important;
    }

    h1, h2, h3 { font-family: 'Cinzel', serif !important; }

    /* ---- HEADER ---- */
    .luxury-header {
        text-align: center;
        padding: 10px 0 5px;
    }
    .luxury-header h1 {
        font-size: 2rem;
        letter-spacing: 0.3em;
        color: var(--gold-light);
        margin: 0;
    }
    .luxury-header p {
        font-size: 0.6rem;
        letter-spacing: 0.3em;
        color: var(--text-muted);
        margin: 4px 0 0;
        text-transform: uppercase;
    }

    /* ---- BUTTONS ---- */
    .stButton > button {
        background: linear-gradient(135deg, #C9A84C, #8B6914) !important;
        color: var(--dark) !important;
        font-family: 'Cinzel', serif !important;
        font-weight: 600 !important;
        letter-spacing: 0.2em !important;
        font-size: 0.75rem !important;
        border: none !important;
        border-radius: 2px !important;
        padding: 12px 20px !important;
        width: 100% !important;
        text-transform: uppercase !important;
    }

    /* Hide Streamlit elements */
    #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ---- UTILS ----
def get_image_base64(path):
    try:
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except:
        return ""

wheel_base64 = get_image_base64("wheel.png")

# ---- SESSION STATE ----
if 'winner_name' not in st.session_state:
    st.session_state.winner_name = ""

# ---- HEADER ----
st.markdown("""
<div class="luxury-header">
    <h1>SKYLUXE</h1>
    <p>Residences &nbsp;·&nbsp; Rewards &nbsp;·&nbsp; Legacy</p>
</div>
""", unsafe_allow_html=True)

# =====================
# 1. LEAD GENERATION
# =====================
if not st.session_state.winner_name:
    st.markdown('<div style="text-align:center; color:var(--gold-light); font-family:Cinzel; font-size:1rem; letter-spacing:0.15em; margin:15px 0;">UNLOCK EXCLUSIVE OFFER</div>', unsafe_allow_html=True)
    
    name = st.text_input("Full Name", placeholder="Enter name")
    phone = st.text_input("Phone Number", placeholder="Enter phone")
    agree = st.checkbox("I agree to terms")

    if st.button("REGISTER & SPIN"):
        if name and phone and agree:
            st.session_state.winner_name = name
            st.rerun()
        else:
            st.error("Please fill all fields.")

# =====================
# 2. GAME PHASE
# =====================
else:
    st.markdown(f"""
    <div style="text-align:center; color:var(--text-muted); font-size:0.8rem; margin-bottom:10px;">
        Welcome, <span style="color:var(--gold-light); font-weight:bold;">{st.session_state.winner_name}</span>
    </div>
    """, unsafe_allow_html=True)

    prizes = [
        {"label": "APPLE IPAD", "icon": "📱"},
        {"label": "BETTER LUCK NEXT TIME", "icon": "❌"},
        {"label": "SPIN AGAIN", "icon": "🔄"},
        {"label": "DOUBLE DOOR REFRIGERATOR", "icon": "❄️"},
        {"label": "SPLIT AIR CONDITIONER", "icon": "💨"},
        {"label": "BETTER LUCK NEXT TIME", "icon": "❌"},
        {"label": "APPLE AIRPODS", "icon": "🎧"},
        {"label": "SPIN AGAIN", "icon": "🔄"}
    ]
    
    prizes_json = json.dumps(prizes)
    
    wheel_html = f"""
    <div id="wrapper" style="display: flex; flex-direction: column; align-items: center; justify-content: center; font-family: 'Raleway', sans-serif;">
        <!-- Pointer -->
        <div id="pointer" style="width: 0; height: 0; border-left: 12px solid transparent; border-right: 12px solid transparent; border-top: 24px solid #C9A84C; z-index: 100; margin-bottom: -10px; filter: drop-shadow(0 0 5px rgba(201,168,76,0.5));"></div>

        <!-- Wheel - Scaled for Mobile -->
        <div id="wheel-container" style="
            position: relative; 
            width: 320px; 
            height: 320px; 
            border-radius: 50%; 
            border: 4px solid #C9A84C; 
            box-shadow: 0 0 30px rgba(201,168,76,0.2);
            background: #000;
            overflow: hidden;
        ">
            <img id="wheel-img" src="data:image/png;base64,{wheel_base64}" style="width: 100%; height: 100%; transition: transform 6s cubic-bezier(0.1, 0, 0, 1); transform: rotate(0deg); border-radius: 50%;">
        </div>

        <!-- Spin Button -->
        <button id="spin-button" style="
            margin-top: 20px; 
            padding: 12px 40px; 
            font-size: 1rem; 
            font-weight: bold; 
            background: linear-gradient(135deg, #C9A84C, #8B6914); 
            color: #0B0C0F; 
            border: none; 
            border-radius: 2px; 
            cursor: pointer; 
            text-transform: uppercase; 
            letter-spacing: 2px;
            font-family: 'Cinzel', serif;
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        ">SPIN FOR PRIZE</button>

        <h2 id="winner-display" style="
            margin-top: 15px; 
            color: #E8C97A; 
            font-family: 'Cinzel', serif; 
            text-align: center; 
            font-size: 1.2rem;
            min-height: 40px;
        "></h2>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <script>
    const prizes = {prizes_json};
    const img = document.getElementById('wheel-img');
    const btn = document.getElementById('spin-button');
    const display = document.getElementById('winner-display');
    let currentRotation = 0;

    btn.addEventListener('click', () => {{
        if(btn.disabled) return;
        btn.disabled = true;
        btn.style.opacity = "0.5";
        display.innerText = "Good Luck...";
        
        const extraDegrees = Math.floor(Math.random() * 360);
        currentRotation += 1800 + extraDegrees;
        img.style.transform = `rotate(${{currentRotation}}deg)`;

        setTimeout(() => {{
            btn.disabled = false;
            btn.style.opacity = "1";
            
            const actualDeg = (currentRotation % 360);
            const numSlices = 8;
            const sliceDeg = 360 / numSlices;
            
            // Pointer is at 12 o'clock (270 degrees)
            const winningIndex = Math.floor(((270 - (actualDeg % 360) + 360) % 360) / sliceDeg);
            const winner = prizes[winningIndex];
            
            display.innerText = "🎉 " + winner.label + " 🎉";
            
            if (!winner.label.includes("BETTER LUCK")) {{
                confetti({{ particleCount: 150, spread: 70, origin: {{ y: 0.6 }}, colors: ['#C9A84C', '#E8C97A', '#FFFFFF'] }});
            }}
        }}, 6100);
    }});
    </script>
    """
    components.html(wheel_html, height=520)

    if st.button("↩ LOGOUT"):
        st.session_state.winner_name = ""
        st.rerun()

st.markdown('<div style="text-align:center; font-size:0.6rem; color:var(--text-muted); margin-top:20px; letter-spacing: 1px;">SKYLUXE RESIDENCES</div>', unsafe_allow_html=True)
