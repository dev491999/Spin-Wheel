import streamlit as st
import random

st.set_page_config(page_title='Lucky Spin Wheel', layout='centered')

st.markdown('''
<style>
@import url("https://fonts.googleapis.com/css2?family=Bangers&display=swap");
body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background: #1a0033 !important;
}
#MainMenu, footer, header, [data-testid="stToolbar"] { visibility: hidden; }
.stButton > button {
    background: linear-gradient(135deg, #FF8C00, #FFD700) !important;
    color: #1a0033 !important;
    font-family: "Bangers", cursive !important;
    font-size: 1.8rem !important;
    letter-spacing: 4px !important;
    border: none !important;
    border-radius: 50px !important;
    padding: 0.5rem 4rem !important;
    width: 100% !important;
    box-shadow: 0 6px 20px #FF8C0066 !important;
    margin-top: 0.5rem !important;
}
</style>
''', unsafe_allow_html=True)

# Segments clockwise from top (index 0 = top segment under pointer at start)
SEGMENTS = [
    {'label': 'APPLE\nIPAD',                  'bg': '#4B0082', 'fg': '#FFD700', 'prize': True},
    {'label': 'BETTER\nLUCK\nNEXT TIME',       'bg': '#F0DEB4', 'fg': '#4B0082', 'prize': False},
    {'label': 'SPIN\nAGAIN',                   'bg': '#4B0082', 'fg': '#FFD700', 'prize': False},
    {'label': 'DOUBLE\nDOOR\nREFRIGERATOR',    'bg': '#F0DEB4', 'fg': '#1a0033', 'prize': True},
    {'label': 'SPLIT AIR\nCONDITIONER',        'bg': '#4B0082', 'fg': '#FFD700', 'prize': True},
    {'label': 'BETTER\nLUCK\nNEXT TIME',       'bg': '#F0DEB4', 'fg': '#4B0082', 'prize': False},
    {'label': 'APPLE\nAIRPODS',                'bg': '#4B0082', 'fg': '#FFFFFF', 'prize': True},
    {'label': 'SPIN\nAGAIN',                   'bg': '#F0DEB4', 'fg': '#FF6600', 'prize': False},
]

N = 8
SLICE = 360.0 / N

for key, val in [('angle', 0.0), ('prev_angle', 0.0), ('spun', False), ('result_idx', -1)]:
    if key not in st.session_state:
        st.session_state[key] = val

segs_json = '['
for i, s in enumerate(SEGMENTS):
    comma = ',' if i < N - 1 else ''
    label_js = s['label'].replace('\n', '\\n')
    prize_js = 'true' if s['prize'] else 'false'
    segs_json += ('{"label":"' + label_js + '","bg":"' + s['bg'] +
                  '","fg":"' + s['fg'] + '","prize":' + prize_js + '}' + comma)
segs_json += ']'

final_angle = st.session_state['angle']
prev_angle  = st.session_state['prev_angle']
spun        = st.session_state['spun']
result_idx  = st.session_state['result_idx']

html_code = (
'<div style="display:flex;flex-direction:column;align-items:center;padding:10px 0;">'

'<div style="position:relative;width:500px;height:520px;">'

# Pointer at very top center - pointing DOWN into wheel
'<div style="position:absolute;top:2px;left:50%;transform:translateX(-50%);z-index:10;">'
'<svg width="44" height="52" viewBox="0 0 44 52">'
'<polygon points="22,52 2,4 42,4" fill="#FFD700" stroke="#8B4513" stroke-width="2.5"/>'
'<polygon points="22,44 8,10 36,10" fill="#FF8C00"/>'
'<circle cx="22" cy="7" r="5" fill="#FFD700" stroke="#8B4513" stroke-width="1.5"/>'
'</svg></div>'

'<canvas id="ringCanvas" width="500" height="500" style="position:absolute;top:20px;left:0;z-index:1;"></canvas>'
'<canvas id="wheelCanvas" width="444" height="444" style="position:absolute;top:48px;left:28px;z-index:2;border-radius:50%;"></canvas>'
'</div>'

'<div id="resultBox" style="display:none;margin-top:10px;padding:14px 32px;border-radius:16px;'
'font-size:1.5rem;letter-spacing:2px;text-align:center;max-width:440px;width:90%;'
'font-family:Bangers,cursive;box-shadow:0 0 30px #FFD70055;"></div>'
'</div>'

'<canvas id="confettiCanvas" style="position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:9999;"></canvas>'

'<script>'
'(function(){'

'var SEGS=' + segs_json + ';'
'var N=8,SLICE=360/N;'

# Marigold ring
'var rc=document.getElementById("ringCanvas");'
'var rctx=rc.getContext("2d");'
'var rcx=rc.width/2,rcy=rc.height/2,flowerR=236,count=54;'
'for(var f=0;f<count;f++){'
'  var a=(f/count)*Math.PI*2-Math.PI/2;'
'  var fx=rcx+Math.cos(a)*flowerR,fy=rcy+Math.sin(a)*flowerR;'
'  for(var p=0;p<6;p++){'
'    var pa=(p/6)*Math.PI*2;'
'    rctx.beginPath();'
'    rctx.ellipse(fx+Math.cos(pa)*6,fy+Math.sin(pa)*6,10,6,pa,0,Math.PI*2);'
'    rctx.fillStyle=f%2===0?"#FF8C00":"#FFA500";rctx.fill();'
'  }'
'  rctx.beginPath();rctx.arc(fx,fy,4,0,Math.PI*2);'
'  rctx.fillStyle="#8B2500";rctx.fill();'
'}'

# Wheel canvas
'var wc=document.getElementById("wheelCanvas");'
'var ctx=wc.getContext("2d");'
'var cx=wc.width/2,cy=wc.height/2,R=wc.width/2-3;'
'function toRad(d){return d*Math.PI/180;}'

'function drawWheel(rot){'
'ctx.clearRect(0,0,wc.width,wc.height);'

'for(var i=0;i<N;i++){'
'  var startA=toRad(rot+i*SLICE-90);'
'  var endA=toRad(rot+(i+1)*SLICE-90);'
'  var midA=toRad(rot+i*SLICE+SLICE/2-90);'
'  var seg=SEGS[i];'

# Slice
'  ctx.beginPath();ctx.moveTo(cx,cy);ctx.arc(cx,cy,R,startA,endA);ctx.closePath();'
'  ctx.fillStyle=seg.bg;ctx.fill();'
'  ctx.strokeStyle="#6B21A8";ctx.lineWidth=2.5;ctx.stroke();'

# Text - always drawn so it reads FROM center OUTWARD, never upside down
'  ctx.save();'
'  ctx.translate(cx,cy);'
# midA is the angle of the segment center. We rotate so text reads outward.
# If segment is on left half (cos < 0), flip 180 so text is not upside down.
'  var cosA=Math.cos(midA);'
'  ctx.rotate(midA);'
# If on left side, rotate 180 and draw text from left (textAlign=left, negative x)
'  var lines=seg.label.split("\\n");'
'  var fs=lines.length<=2?15:12;'
'  ctx.font="900 "+fs+"px Bangers,cursive";'
'  var lh=fs+4;'
'  var totalH=lines.length*lh;'
'  var tr=R*0.72;'
'  if(cosA>=0){'
# Right half: text reads left-to-right outward, align right at tr
'    ctx.textAlign="right";ctx.fillStyle=seg.fg;'
'    for(var l=0;l<lines.length;l++){'
'      ctx.fillText(lines[l],tr,-totalH/2+l*lh+lh*0.75);'
'    }'
'  } else {'
# Left half: flip 180, text reads left-to-right outward from center
'    ctx.rotate(Math.PI);'
'    ctx.textAlign="right";ctx.fillStyle=seg.fg;'
'    for(var l=0;l<lines.length;l++){'
'      ctx.fillText(lines[l],tr,-totalH/2+l*lh+lh*0.75);'
'    }'
'  }'
'  ctx.restore();'
'}'

# Gold outer ring
'ctx.beginPath();ctx.arc(cx,cy,R,0,Math.PI*2);'
'ctx.strokeStyle="#FFD700";ctx.lineWidth=6;ctx.stroke();'

# Inner marigold dot ring
'var dc=40,dr=R-9;'
'for(var d=0;d<dc;d++){'
'  var da=(d/dc)*Math.PI*2;'
'  ctx.beginPath();ctx.arc(cx+Math.cos(da)*dr,cy+Math.sin(da)*dr,4.5,0,Math.PI*2);'
'  ctx.fillStyle=d%2===0?"#FF8C00":"#FFD700";ctx.fill();'
'}'

# Center circle
'ctx.beginPath();ctx.arc(cx,cy,50,0,Math.PI*2);'
'var cg=ctx.createRadialGradient(cx,cy,4,cx,cy,50);'
'cg.addColorStop(0,"#fff");cg.addColorStop(0.5,"#f5e6c8");cg.addColorStop(1,"#c8943a");'
'ctx.fillStyle=cg;ctx.fill();'
'ctx.strokeStyle="#FFD700";ctx.lineWidth=3;ctx.stroke();'
'ctx.beginPath();ctx.arc(cx,cy,42,0,Math.PI*2);'
'ctx.strokeStyle="rgba(160,100,40,0.4)";ctx.lineWidth=1.5;ctx.stroke();'
'ctx.font="bold 36px Georgia,serif";ctx.fillStyle="#8B4513";'
'ctx.textAlign="center";ctx.textBaseline="middle";'
'ctx.fillText("S",cx,cy);'
'}'

# Animation
'var FINAL=' + str(final_angle) + ';'
'var PREV=' + str(prev_angle) + ';'
'var SPUN=' + ('true' if spun else 'false') + ';'
'var RES=' + str(result_idx) + ';'

'drawWheel(FINAL);'

'if(SPUN){animateSpin(PREV,FINAL);}'

'function animateSpin(from,to){'
'  var dur=5500,t0=performance.now();'
'  function ease(t){return 1-Math.pow(1-t,4);}'
'  function frame(now){'
'    var t=Math.min((now-t0)/dur,1);'
'    drawWheel(from+(to-from)*ease(t));'
'    if(t<1){requestAnimationFrame(frame);}else{drawWheel(to);showResult(RES);}'
'  }'
'  requestAnimationFrame(frame);'
'}'

'function showResult(idx){'
'  if(idx<0)return;'
'  var seg=SEGS[idx];'
'  var box=document.getElementById("resultBox");'
'  box.style.display="block";'
'  var label=seg.label.replace(/\\n/g," ");'
'  if(!seg.prize&&label.indexOf("LUCK")!==-1){'
'    box.innerHTML="<span>😔 BETTER LUCK NEXT TIME</span>";'
'    box.style.background="linear-gradient(135deg,#1f1f3a,#2d2d4e)";'
'    box.style.border="3px solid #6b7280";box.style.color="#9ca3af";'
'  }else if(!seg.prize&&label.indexOf("SPIN")!==-1){'
'    box.innerHTML="<span>🔄 SPIN AGAIN!</span>";'
'    box.style.background="linear-gradient(135deg,#2d0057,#4B0082)";'
'    box.style.border="3px solid #a78bfa";box.style.color="#a78bfa";'
'  }else{'
'    box.innerHTML="<span>🎉 YOU WON: "+label+"!</span>";'
'    box.style.background="linear-gradient(135deg,#3d0070,#6a00b8)";'
'    box.style.border="3px solid #FFD700";box.style.color="#FFD700";'
'    launchConfetti();'
'  }'
'}'

'if(!SPUN&&RES>=0){showResult(RES);}'

'function launchConfetti(){'
'  var cc=document.getElementById("confettiCanvas");'
'  cc.width=window.innerWidth;cc.height=window.innerHeight;'
'  var c=cc.getContext("2d");'
'  var cols=["#FFD700","#FF8C00","#7c3aed","#fff","#ff4f94","#00e5ff"],ps=[];'
'  for(var i=0;i<220;i++)ps.push({'
'    x:Math.random()*cc.width,y:-20,'
'    vx:(Math.random()-0.5)*9,vy:Math.random()*5+2,'
'    r:Math.random()*9+4,col:cols[Math.floor(Math.random()*cols.length)],'
'    rot:Math.random()*360,sp:(Math.random()-0.5)*10,'
'    sh:Math.random()>0.5?"r":"c"'
'  });'
'  var fn=0;'
'  function loop(){'
'    c.clearRect(0,0,cc.width,cc.height);var alive=false;'
'    ps.forEach(function(p){'
'      p.x+=p.vx;p.y+=p.vy;p.rot+=p.sp;p.vy+=0.1;'
'      if(p.y<cc.height+30)alive=true;'
'      c.save();c.translate(p.x,p.y);c.rotate(p.rot*Math.PI/180);'
'      c.fillStyle=p.col;'
'      if(p.sh==="r")c.fillRect(-p.r/2,-p.r/2,p.r,p.r*0.5);'
'      else{c.beginPath();c.arc(0,0,p.r/2,0,Math.PI*2);c.fill();}'
'      c.restore();'
'    });'
'    fn++;if(alive&&fn<450)requestAnimationFrame(loop);'
'    else c.clearRect(0,0,cc.width,cc.height);'
'  }'
'  loop();'
'}'

'})();'
'</script>'
)

st.components.v1.html(html_code, height=600)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    spin_btn = st.button('SPIN THE WHEEL', use_container_width=True)

if spin_btn:
    idx = random.randint(0, N - 1)

    # Pointer is at top = 270 degrees in standard math (or -90).
    # Wheel drawn with segment i starting at: rot + i*SLICE - 90 degrees.
    # Segment i center angle in wheel-space = i*SLICE + SLICE/2
    # For segment i center to be at the top (pointer), we need:
    #   rot + i*SLICE + SLICE/2 - 90 = 270  (top in canvas = -90 or 270)
    #   rot = 270 - i*SLICE - SLICE/2 + 90 = 360 - i*SLICE - SLICE/2
    # (mod 360)

    jitter = random.uniform(-SLICE * 0.25, SLICE * 0.25)
    desired_rot_mod = (360 - idx * SLICE - SLICE / 2 + jitter) % 360

    prev = st.session_state['angle']
    cur_mod = prev % 360
    delta = (desired_rot_mod - cur_mod) % 360
    if delta < 90:
        delta += 360

    extra_spins = random.randint(7, 10) * 360
    new_angle = prev + extra_spins + delta

    st.session_state['prev_angle'] = prev
    st.session_state['angle'] = new_angle
    st.session_state['result_idx'] = idx
    st.session_state['spun'] = True
    st.rerun()
