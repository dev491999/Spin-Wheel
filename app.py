import streamlit as st
import streamlit.components.v1 as components
import json

# Prize data extracted from the design document 
prizes = [
    "AIRPODS APPLE",           # [cite: 1]
    "BETTER LUCK NEXT TIME",   # [cite: 2, 3]
    "SPIN AGAIN",              # [cite: 4]
    "IPAD APPLE",              # [cite: 6]
    "DOUBLE DOOR REFRIGERATOR",# [cite: 7, 8, 10]
    "SPLIT AIR CONDITIONER",   # [cite: 9, 10]
    "BETTER LUCK NEXT TIME"    # [cite: 11, 12]
]

st.set_page_config(page_title="Prize Wheel", layout="centered")

# Custom CSS for the Streamlit UI
st.markdown("""
    <style>
    .stApp { background-color: #f4f7f6; }
    .title { text-align: center; color: #2c3e50; font-family: 'Helvetica'; }
    </style>
    <h1 class="title">🎁 Corporate Prize Draw</h1>
""", unsafe_content_html=True)

# The HTML/JavaScript Component
wheel_html = f"""
<div id="container">
    <div id="pointer">▼</div>
    <div id="wheel-wrapper">
        <canvas id="wheel" width="500" height="500"></canvas>
    </div>
    <button id="spin-btn">SPIN TO WIN</button>
    <div id="winner-display"></div>
</div>

<script>
const prizes = {json.dumps(prizes)};
const colors = ["#E74C3C", "#3498DB", "#2ECC71", "#F1C40F", "#9B59B6", "#E67E22", "#1ABC9C"];
const canvas = document.getElementById("wheel");
const ctx = canvas.getContext("2d");
const centerX = canvas.width / 2;
const centerY = canvas.height / 2;
const radius = canvas.width / 2 - 10;

let currentRotation = 0;
let isSpinning = false;

function drawWheel() {{
    const arcSize = (2 * Math.PI) / prizes.length;
    
    prizes.forEach((prize, i) => {{
        const angle = i * arcSize + currentRotation;
        
        // Draw Slice
        ctx.beginPath();
        ctx.fillStyle = colors[i % colors.length];
        ctx.moveTo(centerX, centerY);
        ctx.arc(centerX, centerY, radius, angle, angle + arcSize);
        ctx.lineTo(centerX, centerY);
        ctx.fill();
        ctx.stroke();

        // Draw Text
        ctx.save();
        ctx.translate(centerX, centerY);
        ctx.rotate(angle + arcSize / 2);
        ctx.textAlign = "right";
        ctx.fillStyle = "white";
        ctx.font = "bold 16px Arial";
        // Split text into lines if too long
        const words = prize.split(" ");
        if(words.length > 2) {{
            ctx.fillText(words.slice(0,2).join(" "), radius - 20, -10);
            ctx.fillText(words.slice(2).join(" "), radius - 20, 10);
        }} else {{
            ctx.fillText(prize, radius - 20, 5);
        }}
        ctx.restore();
    }});
}}

document.getElementById("spin-btn").addEventListener("click", () => {{
    if (isSpinning) return;
    isSpinning = true;
    document.getElementById("winner-display").innerText = "Good Luck...";
    
    const spinDuration = 5000;
    const startTimestamp = performance.now();
    const extraSpins = (Math.random() * 5 + 5) * 2 * Math.PI;
    const initialRotation = currentRotation;

    function animate(now) {{
        const elapsed = now - startTimestamp;
        const progress = Math.min(elapsed / spinDuration, 1);
        
        // Easing out function for smooth stop
        const easeOut = 1 - Math.pow(1 - progress, 3);
        currentRotation = initialRotation + (extraSpins * easeOut);
        
        drawWheel();

        if (progress < 1) {{
            requestAnimationFrame(animate);
        }} else {{
            isSpinning = false;
            // Calculate winner based on top pointer (3*PI/2 position)
            const totalSlices = prizes.length;
            const arcSize = (2 * Math.PI) / totalSlices;
            
            // Normalize rotation to 0-2PI
            const normalizedRotation = (currentRotation % (2 * Math.PI));
            // Pointer is at top (1.5 * PI). We find which slice is at that angle.
            const winningIndex = Math.floor(( (1.5 * Math.PI - normalizedRotation + 4 * Math.PI) % (2 * Math.PI) ) / arcSize);
            
            document.getElementById("winner-display").innerText = "WINNER: " + prizes[winningIndex];
        }}
    }}
    requestAnimationFrame(animate);
}});

drawWheel();
</script>

<style>
#container {{ display: flex; flex-direction: column; align-items: center; padding: 20px; }}
#wheel-wrapper {{ position: relative; border: 8px solid #2c3e50; border-radius: 50%; box-shadow: 0 10px 30px rgba(0,0,0,0.3); }}
#pointer {{ 
    font-size: 40px; 
    color: #e74c3c; 
    position: absolute; 
    top: -35px; 
    left: 50%; 
    transform: translateX(-50%); 
    z-index: 100;
    text-shadow: 0 2px 5px rgba(0,0,0,0.5);
}}
#spin-btn {{
    margin-top: 30px;
    padding: 15px 40px;
    font-size: 24px;
    font-weight: bold;
    background: #2ecc71;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    box-shadow: 0 4px #27ae60;
}}
#spin-btn:active {{ transform: translateY(4px); box-shadow: none; }}
#winner-display {{
    margin-top: 20px;
    font-size: 28px;
    font-weight: bold;
    color: #2c3e50;
    height: 40px;
}}
</style>
"""

components.html(wheel_html, height=750)
