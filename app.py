import streamlit as st
import streamlit.components.v1 as components
import random

# 1. Define the prizes from your design document
prizes = [
    "AIRPODS APPLE", 
    "BETTER LUCK NEXT TIME", 
    "SPIN AGAIN", 
    "IPAD APPLE", 
    "DOUBLE DOOR REFRIGERATOR", 
    "SPLIT AIR CONDITIONER",
    "BETTER LUCK NEXT TIME"
]

st.title("🎁 Prize Spin Wheel")
st.subheader("Spin to win your prize!")

# 2. Embed the Spin Wheel using HTML/JS
# This uses a simple CSS/JS wheel logic
wheel_html = f"""
<div id="wrapper">
    <div id="wheel">
        <canvas id="canvas" width="400" height="400"></canvas>
    </div>
    <div id="pointer">▼</div>
    <button id="spin-btn">SPIN</button>
</div>

<script>
const options = {prizes};
const colors = ["#FF5733", "#33FF57", "#3357FF", "#F333FF", "#FF33A1", "#33FFF3", "#F3FF33"];
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
const arc = Math.PI / (options.length / 2);
let startAngle = 0;

function drawWheel() {{
    options.forEach((opt, i) => {{
        const angle = startAngle + i * arc;
        ctx.fillStyle = colors[i % colors.length];
        ctx.beginPath();
        ctx.moveTo(200, 200);
        ctx.arc(200, 200, 200, angle, angle + arc, false);
        ctx.fill();
        ctx.save();
        ctx.fillStyle = "white";
        ctx.translate(200 + Math.cos(angle + arc / 2) * 140, 200 + Math.sin(angle + arc / 2) * 140);
        ctx.rotate(angle + arc / 2 + Math.PI / 2);
        ctx.fillText(opt, -ctx.measureText(opt).width / 2, 0);
        ctx.restore();
    }});
}}

document.getElementById("spin-btn").addEventListener("click", () => {{
    const spinAngle = Math.random() * 10 + 10;
    let currentRotation = 0;
    const interval = setInterval(() => {{
        startAngle += 0.1;
        drawWheel();
        currentRotation += 0.1;
        if (currentRotation >= spinAngle) {{
            clearInterval(interval);
            const index = Math.floor((options.length - (startAngle % (2 * Math.PI)) / arc) % options.length);
            alert("Congratulations! You won: " + options[index]);
        }}
    }}, 10);
}});

drawWheel();
</script>

<style>
#wrapper {{ position: relative; width: 400px; margin: auto; text-align: center; }}
#pointer {{ font-size: 30px; color: red; position: absolute; top: -10px; left: 185px; z-index: 10; }}
#spin-btn {{ margin-top: 20px; padding: 10px 30px; font-size: 20px; cursor: pointer; background: #000; color: #fff; border: none; border-radius: 5px; }}
canvas {{ border-radius: 50%; border: 5px solid #333; }}
</style>
"""

components.html(wheel_html, height=550)

st.info("The prizes are based on the 'Spinwheel Design with Stand' document.")
