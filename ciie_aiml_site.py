# ciie_aiml_site.py
# Run: uvicorn ciie_aiml_site:app --reload --port 8000
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="CIIE AIML Website")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Temporary user store (in memory)
users = {}

# -------------------- Base Template -------------------- #
BASE_HTML = """
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <title>CIIE AIML</title>
  <link rel="icon" type="image/png" href="/static/logo.png">
  <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
    integrity="sha512-aCM+1Nd2N2yQn1g3gK+3o0R9hHc6hC9U1m48v5+/H1/l1Wm3Y0Uuh70q2Gg0L8hjxg2v5D6PPmYJtf3HXpcq9g=="
    crossorigin="anonymous" referrerpolicy="no-referrer" />
  <script src="https://cdnjs.cloudflare.com/ajax/libs/lottie-web/5.10.2/lottie.min.js"></script>
  <style>
    body {
      margin: 0;
      padding: 0;
      font-family: 'Orbitron', Arial, sans-serif;
      color: white;
      background: radial-gradient(circle at 20% 20%, #001133, #000000, #001133);
      background-size: 200% 200%;
      animation: aurora 15s ease-in-out infinite;
      min-height: 100vh;
      min-width: 100vw;
      overflow-x: hidden;
    }

    @keyframes aurora {
      0% {
        background-position: 0% 50%;
        filter: brightness(1);
      }

      50% {
        background-position: 100% 50%;
        filter: brightness(1.2);
      }

      100% {
        background-position: 0% 50%;
        filter: brightness(1);
      }
    }

    header {
      text-align: center;
      padding: 1rem;
      font-size: 2rem;
      font-weight: bold;
      position: relative;
    }

    nav {
      text-align: center;
      background: rgba(255, 255, 255, 0.1);
      padding: 1rem;
      position: sticky;
      top: 0;
      z-index: 1000;
      background: rgba(0, 255, 255, 0.08);
      backdrop-filter: blur(10px);
      border-top: 1px solid rgba(0, 255, 255, 0.3);
      border-bottom: 1px solid rgba(0, 255, 255, 0.3);
    }

    nav a {
      margin: 0 1rem;
      color: white;
      text-decoration: none;
      font-weight: bold;
      position: relative;
      transition: color 0.3s;
    }

    nav a:hover {
      text-decoration: underline;
    }

    nav a.active {
      color: cyan;
    }

    nav a::after {
      content: "";
      position: absolute;
      bottom: -5px;
      left: 0;
      width: 0%;
      height: 2px;
      background-color: cyan;
      transition: width 0.3s;
    }

    nav a.active::after {
      width: 100%;
    }

    nav a:hover::after {
      width: 100%;
    }

    header img {
      position: absolute;
      top: 40px;
      left: 30px;
      height: 180px;
      filter: drop-shadow(0 0 8px cyan);
      transition: transform 0.3s ease;
    }

    header img:hover {
      transform: scale(1.1);
    }

    section {
      margin: 1rem auto;
      width: 90%;
      max-width: 1000px;
      padding: 1rem;
      background: rgba(255,255,255,0.1);
      border-radius: 12px;
      text-align: center;
    }

    h2 {
      margin-bottom: 1rem;
      font-size: 1.8rem;
    }

    form {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 1rem;
    }

    input, button {
      width: 90%;
      max-width: 300px;
    }

    input {
      padding: 0.5rem;
      border-radius: 6px;
      border: 1px solid rgba(255, 255, 255, 0.4);
      background: rgba(0, 0, 0, 0.2);
      color: white;
      transition: 0.3s ease;
    }

    input:focus {
      outline: none;
      border: 1px solid cyan;
      box-shadow: 0 0 10px cyan;
      background: rgba(255, 255, 255, 0.1);
    }

    button {
      padding: 0.5rem 1rem;
      border: none;
      border-radius: 6px;
      background: #ff9800;
      color: white;
      font-weight: bold;
      cursor: pointer;
      transition: all 0.3s ease;
    }

    button:hover {
      background: #e68a00;
      box-shadow: 0 0 15px #ff9800;
      transform: scale(1.05);
    }

    .team {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
      gap: 1rem;
      margin-top: 1rem;
    }

    .card {
      transition: transform 0.3s ease, box-shadow 0.3s ease;
      background: rgba(0, 0, 0, 0.3);
      padding: 1rem;
      border-radius: 8px;
    }

    .card:hover {
      transform: translateY(-5px) scale(1.05);
      box-shadow: 0 0 20px rgba(0, 255, 255, 0.4);
    }

    .card-content {
      margin-bottom: 0.5rem;
    }

    .card-social a {
      color: white;
      margin: 0 0.4rem;
      font-size: 1.2rem;
      transition: color 0.3s;
    }

    .card-social a:hover {
      color: cyan;
    }

    .card.faculty {
      border: 2px solid gold;
      background: linear-gradient(135deg, #FFD700, #FFA500);
      color: #111;
      font-weight: bold;
    }

    .animated-features {
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      justify-content: center;
      margin-top: 2rem;
    }

    .animated-features .feature-box {
      background: rgba(0, 255, 255, 0.2);
      padding: 1rem 2rem;
      border-radius: 12px;
      font-weight: bold;
      min-width: 120px;
      text-align: center;
      cursor: pointer;
      transition: transform 0.3s, background 0.3s, box-shadow 0.3s;
      user-select: none;
      box-shadow: 0 0 5px rgba(0, 255, 255, 0.3);
    }

    .animated-features .feature-box:hover {
      background: rgba(0, 255, 255, 0.5);
      transform: translateY(-5px) scale(1.05);
      box-shadow: 0 0 15px rgba(0, 255, 255, 0.6);
    }

    .animated-text {
      background: linear-gradient(90deg, cyan, violet, pink, cyan);
      -webkit-background-clip: text;
      background-clip: text;
      color: transparent;
      background-size: 200% auto;
      animation: shine 3s linear infinite, fadeIn 1.5s forwards;
    }

    @keyframes shine {
      0% {
        background-position: 0% center;
      }
      100% {
        background-position: 200% center;
      }
    }
    @keyframes fadeIn {
      to {
        opacity: 1;
      }
    }

    #robot-animation {
      width: 150px;
      height: 150px;
      margin: 0 auto;
    }

    h1.animated-text, span {
      margin: 0;
      text-align: center;
    }

    .domain-details {
      margin-top: 1rem;
      background: rgba(0, 255, 255, 0.15);
      padding: 1rem 2rem;
      border-radius: 10px;
      text-align: left;
      max-width: 600px;
      margin-left: auto;
      margin-right: auto;
      box-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
      transition: opacity 0.4s ease, transform 0.4s ease;
      opacity: 0;
      transform: translateY(10px);
      display: none;
    }

    .domain-details.active {
      display: block;
      opacity: 1;
      transform: translateY(0);
    }

    .active-domain {
      background: rgba(0, 255, 255, 0.5) !important;
      box-shadow: 0 0 15px rgba(0, 255, 255, 0.6) !important;
      transform: scale(1.05) !important;
    }

    #glow-bg {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      z-index: -1;
      background: radial-gradient(circle at center, #020213, #000006);
    }

    @media (max-width: 1024px) {
      header img { height: 150px; top:30px; left:20px; }
      h1.animated-text { font-size:3rem; }
      section { width: 95%; padding: 1rem; }
      input, button { max-width: 90%; }
    }

    @media (max-width: 768px) {
      header img { height: 120px; top:25px; left:15px; }
      h1.animated-text { font-size:2.5rem; }
      .animated-features .feature-box { min-width: 80%; padding: 0.75rem 1rem; font-size: 1rem; }
      .domain-details { max-width: 90%; padding: 0.75rem 1rem; font-size: 0.95rem; }
    }

    @media (max-width: 480px) {
      header img { height: 90px; top:20px; left:10px; }
      h1.animated-text { font-size:2rem; }
      section { padding: 0.75rem; }
      .animated-features .feature-box { min-width: 90%; padding: 0.5rem 0.75rem; font-size: 0.9rem; }
      nav a { display: block; margin: 0.5rem 0; font-size: 0.9rem; }
      .domain-details { font-size: 0.9rem; padding: 0.5rem 1rem; }
    }
  </style>
</head>

<body>
  <header>
    <img src="/static/logo.jpg" alt="Logo" style="height:180px; position:absolute; top:40px; left:30px; filter: drop-shadow(0 0 8px cyan); transition: transform 0.3s ease;">
    <div id="robot-animation" style="width:150px; height:150px; margin:0 auto;"></div>
    <h1 class="animated-text" style="font-size:4rem; font-weight:bold; text-align:center; margin:0;">
      AILYTICS CLUB
    </h1>
    <span style="font-size:1rem; font-weight:normal; color:#00ffff; display:block; text-align:center; margin:0;">
      From Curiosity to Creation, THE AIML WAY
    </span>
  </header>
  <nav>
    <a href="/">Home</a>
    <a href="/info">Info</a>
    <a href="/team">Team</a>
    <a href="/login">Login</a>
    <a href="/signup">Signup</a>
  </nav>
  <section>
    {content}
  </section>
  <canvas id="glow-bg"></canvas>
  <script>
    const canvas = document.getElementById("glow-bg");
    const ctx = canvas.getContext("2d");
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    const orbs = [];
    for (let i = 0; i < 20; i++) {
      orbs.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        r: Math.random() * 60 + 20,
        dx: (Math.random() - 0.5) * 0.3,
        dy: (Math.random() - 0.5) * 0.3
      });
    }
    function draw() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      for (const orb of orbs) {
        orb.x += orb.dx; orb.y += orb.dy;
        if (orb.x < 0 || orb.x > canvas.width) orb.dx *= -1;
        if (orb.y < 0 || orb.y > canvas.height) orb.dy *= -1;
        const gradient = ctx.createRadialGradient(orb.x, orb.y, 0, orb.x, orb.y, orb.r);
        gradient.addColorStop(0, "rgba(0,255,255,0.35)");
        gradient.addColorStop(1, "rgba(0,0,0,0)");
        ctx.fillStyle = gradient;
        ctx.fillRect(orb.x - orb.r, orb.y - orb.r, orb.r * 2, orb.r * 2);
        ctx.beginPath();
        ctx.arc(orb.x, orb.y, orb.r * 0.3, 0, Math.PI * 2);
        ctx.strokeStyle = "rgba(0,255,255,0.25)";
        ctx.lineWidth = 1;
        ctx.stroke();
      }
      requestAnimationFrame(draw);
    }
    draw();

    window.addEventListener("scroll", () => {
      canvas.height = Math.max(window.innerHeight, document.body.scrollHeight);
    });
    window.addEventListener("resize", () => {
      canvas.width = window.innerWidth;
      canvas.height = Math.max(window.innerHeight, document.body.scrollHeight);
    });
  </script>
  <script>
    var animation = lottie.loadAnimation({
      container: document.getElementById('robot-animation'),
      renderer: 'svg',
      loop: true,
      autoplay: true,
      path: '/static/robot.json'
    });
  </script>
</body>

</html>
"""

def render(content: str, path: str = "/") -> HTMLResponse:
    """Render content with active navigation highlighting"""
    html = BASE_HTML
    html = html.replace('href="/">', f'href="/" {"class=\"active\"" if path == "/" else ""}>')
    html = html.replace('href="/info">', f'href="/info" {"class=\"active\"" if path == "/info" else ""}>')
    html = html.replace('href="/team">', f'href="/team" {"class=\"active\"" if path == "/team" else ""}>')
    html = html.replace('href="/login">', f'href="/login" {"class=\"active\"" if path == "/login" else ""}>')
    html = html.replace('href="/signup">', f'href="/signup" {"class=\"active\"" if path == "/signup" else ""}>')
    return HTMLResponse(html.replace("{content}", content))

# -------------------- Routes -------------------- #
@app.get("/", response_class=HTMLResponse)
async def home():
    return render("""
<h2 class="animated-text">Welcome to AlLytics AIML Club</h2>
<p class="animated-text" style="animation-delay: 0.5s;">
  Official AI & ML club under CIIE, SRM University Delhi-NCR, Sonepat.
</p>
<p style="text-align:center; font-size:1.2rem; margin-top:1rem; color:#00ffff;">8 Domains. Infinite Possibilities.</p>
<div class="animated-features">
  <div class="feature-box active-domain" data-domain="aiml">AIML</div>
  <div class="feature-box" data-domain="datascience">Data Science</div>
  <div class="feature-box" data-domain="webdev">Web Dev</div>
  <div class="feature-box" data-domain="project">Project</div>
  <div class="feature-box" data-domain="research">Research</div>
  <div class="feature-box" data-domain="socialmedia">Social Media</div>
  <div class="feature-box" data-domain="uiux">UI/UX</div>
  <div class="feature-box" data-domain="workshop">Workshop Training & PR</div>
</div>

<div class="domain-details active" data-domain="aiml">
  <h3>AIML</h3>
  <p>We focus on developing AI & ML projects, learning algorithms, and building intelligent systems.</p>
</div>

<div class="domain-details" data-domain="datascience">
  <h3>Data Science</h3>
  <p>Explore data analysis, visualization, and predictive modeling to extract insights from complex datasets.</p>
</div>

<div class="domain-details" data-domain="webdev">
  <h3>Web Dev</h3>
  <p>Design and develop modern, responsive websites and web applications using the latest technologies.</p>
</div>

<div class="domain-details" data-domain="project">
  <h3>Project</h3>
  <p>Collaborate on innovative projects that solve real-world problems and showcase your skills.</p>
</div>

<div class="domain-details" data-domain="research">
  <h3>Research</h3>
  <p>Engage in cutting-edge research to advance the fields of AI, ML, and related disciplines.</p>
</div>

<div class="domain-details" data-domain="socialmedia">
  <h3>Social Media</h3>
  <p>Manage our online presence, engage the community, and promote club activities through social platforms.</p>
</div>

<div class="domain-details" data-domain="uiux">
  <h3>UI/UX</h3>
  <p>Create user-friendly and appealing interfaces ensuring excellent user experience across platforms.</p>
</div>

<div class="domain-details" data-domain="workshop">
  <h3>Workshop Training & PR</h3>
  <p>Organize workshops, training sessions, and public relations to spread knowledge and grow our community.</p>
</div>

<script>
  const features = document.querySelectorAll('.animated-features .feature-box');
  setInterval(() => {
    features.forEach((f, i) => {
      const y = Math.sin(Date.now() / 1500 + i) * 10;
      f.style.transform = `translateY(${y}px)`;
    });
  }, 16);

  const domainBoxes = document.querySelectorAll('.feature-box');
  const domainDetails = document.querySelectorAll('.domain-details');
  const showDomain = (domainId) => {
    domainDetails.forEach(detail => {
      if (detail.getAttribute('data-domain') === domainId) {
        detail.classList.add('active');
      } else {
        detail.classList.remove('active');
      }
    });
    domainBoxes.forEach(box => {
      if (box.getAttribute('data-domain') === domainId) {
        box.classList.add('active-domain');
      } else {
        box.classList.remove('active-domain');
      }
    });
  };

  domainBoxes.forEach(box => {
    box.addEventListener('click', () => {
      const domainId = box.getAttribute('data-domain');
      showDomain(domainId);
    });
  });
</script>
""", path="/")

@app.get("/info", response_class=HTMLResponse)
async def info():
    return render("""
<h2>About AlLytics Club</h2>
<p>AlLytics Club is the official Artificial Intelligence and Machine Learning club under CIIE at SRM University
  Delhi-NCR, Sonepat. We foster innovation, learning, and collaboration in AI, ML, and Data Science.</p>
<h3>Our Mission</h3>
<ul style="text-align:left; max-width:600px; margin:1rem auto;">
  <li>Bridge the gap between theory and real-world applications.</li>
  <li>Organize workshops, hackathons, research projects, and expert sessions.</li>
  <li>Provide a platform for students to explore emerging technologies and build intelligent solutions.</li>
</ul>
<h3>Key Objectives</h3>
<ul style="text-align:left; max-width:600px; margin:1rem auto;">
  <li>Promote AI & ML literacy through hands-on learning and discussions.</li>
  <li>Encourage practical learning and skill development.</li>
</ul>
<h3>Contact Us</h3>
<ul style="text-align:left; max-width:600px; margin:1rem auto;">
  <li><strong>President:</strong> <a href="tel:+91805571811" style="color:cyan;">Ishita Jaiswal (+91 805571811)</a></li>
  <li><strong>Vice President:</strong> <a href="tel:+917827727574" style="color:cyan;">Prateek Singh (+91 7827727574)</a></li>
  <li><strong>Email:</strong> <a href="mailto:ciieaimicommunity@gmail.com" style="color:cyan;">ciieaimicommunity@gmail.com</a></li>
</ul>
<h3>Our Social Media Handles</h3>
<div style="display:flex; justify-content:center; gap:1rem; font-size:1.5rem; margin-top:0.5rem;">
  <a href="https://www.instagram.com/clle_aiml_community" target="_blank" style="color:white;">
    <i class="fab fa-instagram"></i>
  </a>
  <a href="https://www.linkedin.com/cile-aiml-community" target="_blank" style="color:white;">
    <i class="fab fa-linkedin"></i>
  </a>
</div>
<p>Follow our Instagram: <a href="https://www.instagram.com/ciie_aiml_community" target="_blank"
    style="color:cyan;">@ciie_aiml_community</a></p>
<p>Follow our LinkedIn: <a href="https://www.linkedin.com/company/ciie-aiml-community/" target="_blank" style="color:cyan;">CIIE AIML Community</a></p>
""", path="/info")

@app.get("/team", response_class=HTMLResponse)
async def team():
    return render("""
<h2>Our Team</h2>
<h3>Faculty Mentors</h3>
<div class="team">
  <div class="card faculty">
    <div class="card-content">
      <strong>Atif Sir</strong><br>Faculty Mentor
    </div>
  </div>
  <div class="card faculty">
    <div class="card-content">
      <strong>Ahmed Sir</strong><br>Faculty Mentor
    </div>
  </div>
</div>
<h3>Core Members</h3>
<div class="team">
  <div class="card">
    <div class="card-content">
      <strong>Arpita</strong><br>Web Dev Lead
    </div>
    <div class="card-social">
      <a href="#" target="_blank"><i class="fab fa-linkedin"></i></a>
      <a href="#" target="_blank"><i class="fab fa-github"></i></a>
    </div>
  </div>
  <div class="card">
    <div class="card-content">
      <strong>Shubham</strong><br>App Dev Lead
    </div>
    <div class="card-social">
      <a href="#" target="_blank"><i class="fab fa-linkedin"></i></a>
      <a href="#" target="_blank"><i class="fab fa-github"></i></a>
    </div>
  </div>
  <div class="card">
    <div class="card-content">
      <strong>Arshiya</strong><br>Research Head
    </div>
    <div class="card-social">
      <a href="#" target="_blank"><i class="fab fa-linkedin"></i></a>
      <a href="#" target="_blank"><i class="fab fa-github"></i></a>
    </div>
  </div>
  <div class="card">
    <div class="card-content">
      <strong>Rajveer</strong><br>Workshop Lead
    </div>
    <div class="card-social">
      <a href="#" target="_blank"><i class="fab fa-linkedin"></i></a>
      <a href="#" target="_blank"><i class="fab fa-github"></i></a>
    </div>
  </div>
  <div class="card">
    <div class="card-content">
      <strong>Ishita</strong><br>Data Science & Design
    </div>
    <div class="card-social">
      <a href="#" target="_blank"><i class="fab fa-linkedin"></i></a>
      <a href="#" target="_blank"><i class="fab fa-github"></i></a>
    </div>
  </div>
  <div class="card">
    <div class="card-content">
      <strong>Trisha</strong><br>Marketing Lead
    </div>
    <div class="card-social">
      <a href="#" target="_blank"><i class="fab fa-linkedin"></i></a>
      <a href="#" target="_blank"><i class="fab fa-github"></i></a>
    </div>
  </div>
  <div class="card">
    <div class="card-content">
      <strong>Nitan</strong><br>Project Lead
    </div>
    <div class="card-social">
      <a href="#" target="_blank"><i class="fab fa-linkedin"></i></a>
      <a href="#" target="_blank"><i class="fab fa-github"></i></a>
    </div>
  </div>
  <div class="card">
    <div class="card-content">
      <strong>Prateek</strong><br>AIML Lead
    </div>
    <div class="card-social">
      <a href="#" target="_blank"><i class="fab fa-linkedin"></i></a>
      <a href="#" target="_blank"><i class="fab fa-github"></i></a>
    </div>
  </div>
</div>
""", path="/team")

# -------------------- Login -------------------- #
@app.get("/login", response_class=HTMLResponse)
async def login_form():
    return render("""
<h2>Login</h2>
<form action="/login" method="post">
  <input type="text" name="username" placeholder="Enter Username" required>
  <input type="password" name="password" placeholder="Enter Password" required>
  <button type="submit">Login</button>
</form>
""", path="/login")

@app.post("/login", response_class=HTMLResponse)
async def login(username: str = Form(...), password: str = Form(...)):
    if username not in users or users[username] != password:
        return render("<h3 style='color:tomato'>Invalid username or password</h3>", path="/login")
    return render(f"<h3 style='color:lightgreen'>Welcome back, {username}!</h3>", path="/login")

# -------------------- Signup -------------------- #
@app.get("/signup", response_class=HTMLResponse)
async def signup_form():
    return render("""
<h2>Signup</h2>
<form action="/signup" method="post">
  <input type="text" name="username" placeholder="Choose Username" required>
  <input type="password" name="password" placeholder="Choose Password" required>
  <button type="submit">Signup</button>
</form>
""", path="/signup")

@app.post("/signup", response_class=HTMLResponse)
async def signup(username: str = Form(...), password: str = Form(...)):
    if username in users:
        return render("<h3 style='color:tomato'>Username already exists</h3>", path="/signup")
    users[username] = password
    return render(f"<h3 style='color:lightgreen'>Thanks for signing up, {username}!</h3>", path="/signup")
