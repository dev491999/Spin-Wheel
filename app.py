import streamlit as st
import streamlit.components.v1 as components
import json

# Prize data with the same UI logic but updated vibrant premium colors
prizes = [
    {"label": "AIRPODS APPLE", "img": "🎧", "color": "#2c3e50", "text": "#ffffff"}, # Midnight Slate
    {"label": "BETTER LUCK", "img": "🍀", "color": "#d4af37", "text": "#000000"},    # Metallic Gold
    {"label": "SPIN AGAIN", "img": "🔄", "color": "#27ae60", "text": "#ffffff"},    # Emerald Green
    {"label": "IPAD APPLE", "img": "📱", "color": "#2980b9", "text": "#ffffff"},    # Royal Blue
    {"label": "REFRIGERATOR", "img": "🧊", "color": "#d4af37", "text": "#000000"}, # Metallic Gold
    {"label": "AIR CONDITIONER", "img": "❄️", "color": "#8e44ad", "text": "#ffffff"}, # Royal Purple
    {"label": "BETTER LUCK", "img": "✨", "color": "#c0392b", "text": "#ffffff"}     # Deep Ruby
]

st.set_page_config(page_title="Premium Rewards", layout="centered")

# App Styling
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp {background-color: #0e1117;}
    </style>
""", unsafe_allow_html=True)

wheel_html = f"""
<div id="app-container" style="background: radial-gradient(circle, #1c2833 0%, #000000 100%); padding: 40px; border-radius: 20px; display: flex; flex-direction: column; align-items: center; box-shadow: 0 20px 50px rgba(0,0,0,0.7);">
    
    <div id="pointer" style="
        position: relative; z-index: 10;
        width: 40px; height: 40px; 
        background: #ffffff; clip-path: polygon(50% 100%, 0 0, 100% 0);
        filter: drop-shadow(0 0 10px rgba(255,255,255,0.5));
        margin-bottom: -15px;
    "></div>

    <div id="wheel-case" style="
        padding: 15px; background: linear-gradient(145deg, #d4af37, #8a6d3b); 
        border-radius: 50%; box-shadow: inset 0 0 20px rgba(0,0,0,0.8), 0 10px 30px rgba(0,0,0,0.6);
    ">
        <canvas id="wheel" width="500" height="500" style="border-radius: 50%;"></canvas>
    </div>

    <button id="spin-btn" style="
        margin-top: 40px; padding: 15px 60px; font-size: 24px; font-weight: 900;
        text-transform: uppercase; letter-spacing: 2px;
        background: linear-gradient(to right, #d4af37, #f7e681);
        border: none; border-radius: 50px; cursor: pointer;
        color: #000; box-shadow: 0 10px 20px rgba(0,0,0,0.4);
        transition: all 0.2s ease;
    ">Spin to Win</button>

    <h1 id="status" style="color: #d4af37; font-family: 'Georgia', serif; margin-top: 30px; letter-spacing: 1px; min-height: 50px; text-align: center;"></h1>
</div>

<script>
const prizes = {json.dumps(prizes)};
const canvas = document.getElementById('wheel');
const ctx = canvas.getContext('2d');
const btn = document.getElementById('spin-btn');
const status = document.getElementById('status');

const centerX = 250;
const centerY = 250;
const radius = 250;
const sliceAngle = (2 * Math.PI) / prizes.length;

let currentRotation = 0;

function drawWheel() {{
    ctx.clearRect(0,0,500,500);
    
    prizes.forEach((p, i) => {{
        const angle = i * sliceAngle + currentRotation;
        
        // Premium 3D Slice Gradient
        const grad = ctx.createRadialGradient(centerX, centerY, 0, centerX, centerY, radius);
        grad.addColorStop(0, p.color);
        grad.addColorStop(0.8, p.color);
        grad.addColorStop(1, "#000000"); // Depth effect at edge
        
        ctx.beginPath();
        ctx.fillStyle = grad;
        ctx.moveTo(centerX, centerY);
        ctx.arc(centerX, centerY, radius, angle, angle + sliceAngle);
        ctx.fill();
        ctx.strokeStyle = "rgba(255,255,255,0.1)";
        ctx.lineWidth = 2;
        ctx.stroke();

        // Optimized Text Placement
        ctx.save();
        ctx.translate(centerX, centerY);
        ctx.rotate(angle + sliceAngle / 2);
        ctx.textAlign = "right";
        ctx.fillStyle = p.text;
        
        // Draw Label
        ctx.font = "bold 16px sans-serif";
        ctx.shadowBlur = 4;
        ctx.shadowColor = "rgba(0,0,0,0.8)";
        ctx.fillText(p.label, radius - 70, 8);
        
        // Draw Icon
        ctx.font = "28px Arial";
        ctx.fillText(p.img, radius - 25, 12);
        ctx.restore();
    }});

    // Center Decorative Hub
    ctx.beginPath();
    ctx.arc(centerX, centerY, 35, 0, 2*Math.PI);
    ctx.fillStyle = "#222";
    ctx.fill();
    ctx.strokeStyle = "#d4af37";
    ctx.lineWidth = 4;
    ctx.stroke();
    ctx.fillStyle = "#d4af37";
    ctx.font = "20px Arial";
    ctx.textAlign = "center";
    ctx.fillText("🎁", centerX, centerY + 7);
}}

btn.onclick = () => {{
    if(btn.disabled) return;
    btn.disabled = true;
    btn.style.opacity = "0.5";
    status.innerText = "⭐ GOOD LUCK ⭐";
    
    const spins = 8 + Math.random() * 5; 
    const totalRotation = spins * 2 * Math.PI;
    const duration = 7000; 
    const start = performance.now();
    const initialRotation = currentRotation;

    function animate(now) {{
        const elapsed = now - start;
        const t = Math.min(elapsed / duration, 1);
        
        // Smooth Cubic Easing
        const easeOut = 1 - Math.pow(1 - t, 4);
        
        currentRotation = initialRotation + (totalRotation * easeOut);
        drawWheel();

        if (t < 1) {{
            requestAnimationFrame(animate);
        }} else {{
            btn.disabled = false;
            btn.style.opacity = "1";
            
            const normalized = (currentRotation % (2 * Math.PI));
            // Calculating winning slice relative to 12 o'clock pointer
            const winningIndex = Math.floor(((1.5 * Math.PI - normalized + (10 * Math.PI)) % (2 * Math.PI)) / sliceAngle);
            status.innerHTML = "🏆 WINNER: " + prizes[winningIndex].label;
        }}
    }}
    requestAnimationFrame(animate);
}};

drawWheel();
</script>
"""

components.html(wheel_html, height=850)
