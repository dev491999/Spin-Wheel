import streamlit as st
import streamlit.components.v1 as components

# Prize list based on the provided design document
# Note: "Better Luck Next Time" appears twice in the source to fill the wheel segments
prizes = [
    "AIRPODS APPLE",            # Source 1
    "BETTER LUCK NEXT TIME",    # Source 2, 3
    "SPIN AGAIN",               # Source 4, 5
    "IPAD APPLE",               # Source 6
    "DOUBLE DOOR REFRIGERATOR", # Source 7, 8, 10
    "SPLIT AIR CONDITIONER",    # Source 9, 10
    "BETTER LUCK NEXT TIME"     # Source 11, 12
]

st.set_page_config(page_title="Premium Prize Wheel", layout="centered")
st.title("🎡 Spin to Win!")

# HTML, CSS, and JS for the animated wheel
wheel_html = f"""
<div class="main-container">
    <div class="pointer">▼</div>
    <div class="wheel-outer">
        <div id="wheel" class="wheel"></div>
    </div>
    <button id="spin-btn">SPIN WHEEL</button>
    <h2 id="result-display"></h2>
</div>

<style>
    .main-container {{
        display: flex;
        flex-direction: column;
        align-items: center;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}
    .pointer {{
        font-size: 50px;
        color: #e74c3c;
        line-height: 1;
        z-index: 10;
        margin-bottom: -20px;
        text-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }}
    .wheel-outer {{
        width: 450px;
        height: 450px;
        border: 10px solid #333;
        border-radius: 50%;
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
    }}
    .wheel {{
        width: 100%;
        height: 100%;
        border-radius: 50%;
        position: relative;
        transition: transform 5s cubic-bezier(0.15, 0, 0.15, 1); /* Smooth deceleration */
    }}
    #spin-btn {{
        margin-top: 30px;
        padding: 15px 40px;
        font-size: 20px;
        font-weight: bold;
        background-color: #2ecc71;
        color: white;
        border: none;
        border-radius: 50px;
        cursor: pointer;
        transition: 0.3s;
        box-shadow: 0 5px 15px rgba(46, 204, 113, 0.4);
    }}
    #spin-btn:hover {{ background-color: #27ae60; transform: scale(1.05); }}
    #result-display {{ margin-top: 20px; color: #333; height: 40px; }}
</style>

<script>
    const prizes = {prizes};
    const wheel = document.getElementById('wheel');
    const btn = document.getElementById('spin-btn');
    const result = document.getElementById('result-display');
    const numSegments = prizes.length;
    const anglePerSegment = 360 / numSegments;
    const colors = ['#f1c40f', '#e67e22', '#e74c3c', '#9b59b6', '#3498db', '#1abc9c', '#2ecc71'];

    // Draw the segments
    let segmentsHtml = '';
    for (let i = 0; i < numSegments; i++) {{
        const rotation = i * anglePerSegment;
        segmentsHtml += `
            <div style="
                position: absolute;
                width: 50%;
                height: 50%;
                background-color: ${{colors[i % colors.length]}};
                transform-origin: 100% 100%;
                transform: rotate(${{rotation}}deg) skewY(${{90 - anglePerSegment}}deg);
                border: 1px solid rgba(255,255,255,0.2);
            "></div>
            <div style="
                position: absolute;
                width: 50%;
                height: 50%;
                left: 50%;
                top: 50%;
                transform-origin: 0 0;
                transform: rotate(${{rotation + anglePerSegment/2}}deg) translateY(-160px);
                text-align: center;
                color: white;
                font-weight: bold;
                font-size: 14px;
                width: 120px;
                margin-left: -60px;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
            ">${{prizes[i]}}</div>
        `;
    }}
    wheel.innerHTML = segmentsHtml;

    let currentRotation = 0;

    btn.addEventListener('click', () => {{
        btn.disabled = true;
        result.innerText = "Spinning...";
        
        // Random spin between 5 and 10 full rotations + random segment
        const extraDegrees = Math.floor(Math.random() * 360);
        const spinTotal = 1800 + extraDegrees; 
        currentRotation += spinTotal;
        
        wheel.style.transform = `rotate(${{currentRotation}}deg)`;

        setTimeout(() => {{
            btn.disabled = false;
            // Calculate winning index (Pointer is at top, which is 0 degrees in CSS)
            // We need to account for the cumulative rotation
            const actualDegree = currentRotation % 360;
            const winningIndex = Math.floor((360 - actualDegree) / anglePerSegment) % numSegments;
            result.innerText = "Winner: " + prizes[winningIndex];
        }}, 5000);
    }});
</script>
"""

components.html(wheel_html, height=700)
