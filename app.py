import streamlit as st
import streamlit.components.v1 as components
import json

# Prize list based on your PDF design
prizes = [
    "AIRPODS APPLE",
    "BETTER LUCK NEXT TIME",
    "SPIN AGAIN",
    "IPAD APPLE",
    "DOUBLE DOOR REFRIGERATOR",
    "SPLIT AIR CONDITIONER",
    "BETTER LUCK NEXT TIME"
]

st.set_page_config(page_title="Prize Wheel", layout="centered")

# Using a standard st.title to avoid the markdown error
st.title("🎁 Corporate Prize Draw")

# Hex colors matching a premium look
colors = ["#E74C3C", "#3498DB", "#2ECC71", "#F1C40F", "#9B59B6", "#E67E22", "#1ABC9C"]

# The HTML/JS component
wheel_html = f"""
<div id="wrapper" style="display: flex; flex-direction: column; align-items: center; font-family: sans-serif;">
    <div id="pointer" style="font-size: 40px; color: #ff0000; z-index: 10; margin-bottom: -30px;">▼</div>
    <canvas id="wheel" width="500" height="500" style="border-radius: 50%; border: 5px solid #333; box-shadow: 0 10px 20px rgba(0,0,0,0.2);"></canvas>
    <button id="spin-btn" style="margin-top: 20px; padding: 15px 40px; font-size: 20px; cursor: pointer; background: #2ecc71; color: white; border: none; border-radius: 5px; font-weight: bold;">SPIN WHEEL</button>
    <h2 id="winner-text" style="margin-top: 20px; color: #2c3e50; min-height: 40px;"></h2>
</div>

<script>
const prizes = {json.dumps(prizes)};
const colors = {json.dumps(colors)};
const canvas = document.getElementById("wheel");
const ctx = canvas.getContext("2d");
const centerX = 250;
const centerY = 250;
const radius = 240;
const numSlices = prizes.length;
const sliceAngle = (2 * Math.PI) / numSlices;

let currentRotation = 0;

function drawWheel() {{
    ctx.clearRect(0, 0, 500, 500);
    for (let i = 0; i < numSlices; i++) {{
        const angle = i * sliceAngle + currentRotation;
        
        // Draw Slice
        ctx.beginPath();
        ctx.fillStyle = colors[i % colors.length];
        ctx.moveTo(centerX, centerY);
        ctx.arc(centerX, centerY, radius, angle, angle + sliceAngle);
        ctx.lineTo(centerX, centerY);
        ctx.fill();
        ctx.strokeStyle = "white";
        ctx.stroke();

        // Draw Text
        ctx.save();
        ctx.translate(centerX, centerY);
        ctx.rotate(angle + sliceAngle / 2);
        ctx.textAlign = "right";
        ctx.fillStyle = "white";
        ctx.font = "bold 16px Arial";
        ctx.fillText(prizes[i], radius - 20, 10);
        ctx.restore();
    }}
}}

document.getElementById("spin-btn").onclick = function() {{
    const btn = this;
    btn.disabled = true;
    const winnerDisplay = document.getElementById("winner-text");
    winnerDisplay.innerText = "Spinning...";

    const spinSpins = 5 + Math.random() * 5; // 5 to 10 full rotations
    const totalRotation = spinSpins * 2 * Math.PI;
    const duration = 5000;
    const start = performance.now();

    const initialRotation = currentRotation;

    function animate(now) {{
        const elapsed = now - start;
        const t = Math.min(elapsed / duration, 1);
        
        // Cubic ease-out for smooth stopping
        const easeOut = 1 - Math.pow(1 - t, 3);
        
        currentRotation = initialRotation + (totalRotation * easeOut);
        drawWheel();

        if (t < 1) {{
            requestAnimationFrame(animate);
        }} else {{
            btn.disabled = false;
            
            // MATH FOR TOP POINTER:
            // The pointer is at 1.5 * PI (270 degrees). 
            // We normalize rotation and find which slice is under the pointer.
            const normalizedRotation = (currentRotation % (2 * Math.PI));
            const winningIndex = Math.floor(((1.5 * Math.PI - normalizedRotation + (4 * Math.PI)) % (2 * Math.PI)) / sliceAngle);
            
            winnerDisplay.innerText = "WINNER: " + prizes[winningIndex];
        }}
    }}
    requestAnimationFrame(animate);
}};

drawWheel();
</script>
"""

components.html(wheel_html, height=700)
