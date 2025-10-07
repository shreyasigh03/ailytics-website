
# ciie_aiml_site.py
# Run: uvicorn ciie_aiml_site:app --reload --port 8000
## -*- coding: utf-8 -*-
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from typing import Optional
from datetime import datetime
import os

app = FastAPI(title="CIIE AIML Website")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Temporary user store (in memory)
users = {}
# Event registrations store (in memory)
event_registrations = []

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
      background: rgba(255, 255, 255, 0.1);
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

    input,
    button,
    select {
      width: 90%;
      max-width: 300px;
    }

    input,
    select {
      padding: 0.5rem;
      border-radius: 6px;
      border: 1px solid rgba(255, 255, 255, 0.4);
      background: rgba(0, 0, 0, 0.2);
      color: white;
      transition: 0.3s ease;
      font-family: 'Orbitron', Arial, sans-serif;
    }

    input:focus,
    select:focus {
      outline: none;
      border: 1px solid cyan;
      box-shadow: 0 0 10px cyan;
      background: rgba(255, 255, 255, 0.1);
    }

    select option {
      background: #001133;
      color: white;
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
      grid-template-columns: repeat(3, 1fr);
      gap: 1.5rem;
      margin-top: 1rem;
    }

    .card {
      min-height: 220px; /* increased height for better spacing */
      padding: 1.5rem;
      transition: transform 0.3s ease, box-shadow 0.3s ease;
      background: rgba(0, 0, 0, 0.3);
      border-radius: 8px;
    }

    .card-content img {
      width: 80px;   /* increased image size */
      height: 80px;
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

    h1.animated-text,
    span {
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

    /* Modal Styles */
    .modal {
      display: none;
      position: fixed;
      z-index: 2000;
      left: 0;
      top: 0;
      width: 100%;
      height: 100%;
      overflow: auto;
      background-color: rgba(0, 0, 0, 0.8);
      backdrop-filter: blur(10px);
      animation: fadeIn 0.3s ease;
    }

    .modal-content {
      background: linear-gradient(135deg, rgba(0, 17, 51, 0.95), rgba(0, 0, 0, 0.95));
      margin: 3% auto;
      padding: 2rem;
      border: 2px solid rgba(0, 255, 255, 0.4);
      border-radius: 15px;
      width: 90%;
      max-width: 500px;
      box-shadow: 0 0 30px rgba(0, 255, 255, 0.5);
      animation: slideIn 0.4s ease;
      position: relative;
    }

    @keyframes slideIn {
      from {
        transform: translateY(-50px);
        opacity: 0;
      }

      to {
        transform: translateY(0);
        opacity: 1;
      }
    }

    .close {
      color: #00ffff;
      float: right;
      font-size: 2rem;
      font-weight: bold;
      cursor: pointer;
      transition: all 0.3s ease;
      line-height: 1;
      margin-top: -0.5rem;
    }

    .close:hover,
    .close:focus {
      color: #ff9800;
      transform: rotate(90deg) scale(1.2);
    }

    .modal h2 {
      color: #00ffff;
      text-align: center;
      margin-bottom: 1.5rem;
      font-size: 1.8rem;
      text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
    }

    .modal form {
      width: 100%;
    }

    .modal input,
    .modal select {
      width: 100%;
      max-width: 100%;
      margin-bottom: 1rem;
      padding: 0.8rem;
      font-size: 0.95rem;
    }

    .modal label {
      display: block;
      margin-bottom: 0.3rem;
      color: #00ffff;
      font-size: 0.9rem;
      text-align: left;
    }

    .modal button[type="submit"] {
      width: 100%;
      max-width: 100%;
      padding: 1rem;
      font-size: 1.1rem;
      background: linear-gradient(135deg, #00ffff, #0080ff);
      margin-top: 1rem;
    }

    .modal button[type="submit"]:hover {
      background: linear-gradient(135deg, #0080ff, #00ffff);
      box-shadow: 0 0 20px rgba(0, 255, 255, 0.6);
    }

    .form-group {
      margin-bottom: 1rem;
      text-align: left;
    }

    .required {
      color: #ff9800;
    }

    @media (max-width: 1024px) {
      header img {
        height: 150px;
        top: 30px;
        left: 20px;
      }

      h1.animated-text {
        font-size: 3rem;
      }

      section {
        width: 95%;
        padding: 1rem;
      }

      input,
      button {
        max-width: 90%;
      }

      .modal-content {
        width: 85%;
        margin: 5% auto;
      }
    }

    @media (max-width: 768px) {
      header img {
        height: 120px;
        top: 30px;
        left: 18px;
      }

      h1.animated-text {
        font-size: 2.5rem;
        margin-top: 70px;
      }

      .animated-features {
        margin-top: 2.5rem;
      }

      .animated-features .feature-box {
        min-width: 80%;
        padding: 0.9rem 1.1rem;
        font-size: 1.08rem;
      }

      .domain-details {
        max-width: 95%;
        padding: 1rem 1.2rem;
        font-size: 1rem;
        margin-bottom: 1.5rem;
      }

      .modal-content {
        width: 90%;
        padding: 1.5rem;
        margin: 10% auto;
      }

      nav a {
        margin: 0.7rem 0.6rem;
        font-size: 1.2rem;
        padding: 0.6rem 1.4rem;
        display: inline-block;
      }

      input,
      button,
      select {
        max-width: 95%;
        width: 95%;
      }

      section {
        width: 98%;
        padding: 0.8rem;
      }

      /* Responsive team/event cards and grid for <=768px */
      .team {
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
      }
      .animated-team .card, .animated-events .card {
        width: 45%;
        height: auto;
      }
    }

    @media (max-width: 480px) {
      header img {
        height: 100px;
        top: 24px;
        left: 12px;
      }

      h1.animated-text {
        font-size: 2.5rem;
        margin-top: 100px;
      }

      section {
        width: 99%;
        padding: 0.5rem;
        margin: 0.5rem auto;
      }

      /* Enhanced responsiveness for team, events, and features */
      .animated-team .card, .animated-events .card {
        width: 90%;
        height: auto;
        margin: 0.8rem auto;
      }
      .animated-team, .animated-events {
        flex-direction: column;
        align-items: center;
        gap: 1rem;
      }
      .team {
        grid-template-columns: repeat(1, 1fr);
        gap: 1rem;
      }
      .animated-features {
        margin-top: 2.8rem;
        gap: 1rem;
      }
      .feature-box {
        width: 90%;
      }
      h2, h3 {
        font-size: 1.4rem;
      }

      .animated-features .feature-box {
        min-width: 95%;
        padding: 0.7rem 0.9rem;
        font-size: 1.05rem;
      }

      nav a {
        display: inline-block;
        margin: 0.7rem 0.25rem;
        font-size: 1.2rem;
        padding: 0.7rem 1.2rem;
        line-height: 1.6;
      }

      .domain-details {
        font-size: 1rem;
        padding: 0.7rem 1.1rem;
        margin-bottom: 1.5rem;
      }

      .modal-content {
        width: 98%;
        padding: 0.6rem;
        margin: 12% auto;
      }

      .modal h2 {
        font-size: 1.5rem;
      }

      input,
      button,
      select {
        max-width: 95%;
        width: 95%;
      }
    }
  </style>
</head>

<body>
  <header>
    <img src="/static/logo.jpg" alt="Logo"
      style="height:180px; position:absolute; top:40px; left:30px; filter: drop-shadow(0 0 8px cyan); transition: transform 0.3s ease;">
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
    <a href="/events">Events</a>
    <a href="/login">Login</a>
    <a href="/signup">Signup</a>
  </nav>
  <section>
    {content}
  </section>

  <!-- Event Registration Modal -->
  <div id="registrationModal" class="modal">
    <div class="modal-content">
      <span class="close" onclick="closeRegistrationModal()">&times;</span>
      <h2><i class="fas fa-calendar-plus" style="margin-right:0.5rem;"></i>Event Registration</h2>
      <form action="/register-event" method="post" onsubmit="return validateForm()">
        <div class="form-group">
          <label for="fullname">Full Name <span class="required">*</span></label>
          <input type="text" id="fullname" name="fullname" placeholder="Enter your full name" required>
        </div>

        <div class="form-group">
          <label for="course">Course <span class="required">*</span></label>
          <input type="text" id="course" name="course" placeholder="e.g., B.Tech CSE, BCA, MCA" required>
        </div>

        <div class="form-group">
          <label for="year_semester">Year/Semester <span class="required">*</span></label>
          <select id="year_semester" name="year_semester" required>
            <option value="">Select Year/Semester</option>
            <option value="1st Year / 1st Semester">1st Year / 1st Semester</option>
            <option value="1st Year / 2nd Semester">1st Year / 2nd Semester</option>
            <option value="2nd Year / 3rd Semester">2nd Year / 3rd Semester</option>
            <option value="2nd Year / 4th Semester">2nd Year / 4th Semester</option>
            <option value="3rd Year / 5th Semester">3rd Year / 5th Semester</option>
            <option value="3rd Year / 6th Semester">3rd Year / 6th Semester</option>
            <option value="4th Year / 7th Semester">4th Year / 7th Semester</option>
            <option value="4th Year / 8th Semester">4th Year / 8th Semester</option>
          </select>
        </div>

        <div class="form-group">
          <label for="phone">Phone Number <span class="required">*</span></label>
          <input type="tel" id="phone" name="phone" placeholder="Enter 10-digit mobile number" pattern="[0-9]{10}"
            required>
        </div>

        <div class="form-group">
          <label for="email">Email (Optional)</label>
          <input type="email" id="email" name="email" placeholder="your.email@example.com">
        </div>

        <div class="form-group">
          <label for="event">Select Event <span class="required">*</span></label>
          <select id="event" name="event" required>
            <option value="">Choose an event</option>
            <option value="AI Hackathon 2025">AI Hackathon 2025</option>
            <option value="Machine Learning Workshop"> Machine Learning Workshop</option>
            <option value="Data Science Bootcamp">Data Science Bootcamp</option>
            <option value="AI Innovation Summit"> AI Innovation Summit</option>
            <option value="Python Programming Session"> Python Programming Session</option>
            <option value="Deep Learning Masterclass"> Deep Learning Masterclass</option>
          </select>
        </div>

        <button type="submit">
          <i class="fas fa-paper-plane" style="margin-right:0.5rem;"></i>Submit Registration
        </button>
      </form>
    </div>
  </div>

  <canvas id="glow-bg"></canvas>
  <script>
    // Canvas animation
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

    // Modal functions
    function openRegistrationModal() {
      document.getElementById('registrationModal').style.display = 'block';
      document.body.style.overflow = 'hidden';
    }

    function closeRegistrationModal() {
      document.getElementById('registrationModal').style.display = 'none';
      document.body.style.overflow = 'auto';
    }

    // Close modal when clicking outside
    window.onclick = function (event) {
      const modal = document.getElementById('registrationModal');
      if (event.target == modal) {
        closeRegistrationModal();
      }
    }

    // Form validation
    function validateForm() {
      const phone = document.getElementById('phone').value;
      const phonePattern = /^[0-9]{10}$/;

      if (!phonePattern.test(phone)) {
        alert('Please enter a valid 10-digit phone number');
        return false;
      }

      return true;
    }

    // Close modal on Escape key
    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape') {
        closeRegistrationModal();
      }
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
    html = html.replace('href="/events">', f'href="/events" {"class=\"active\"" if path == "/events" else ""}>')
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
  <li><strong>Vice President:</strong> <a href="tel:+917827727574" style="color:cyan;">Prateek Singh (+91
      7827727574)</a></li>
  <li><strong>Email:</strong> <a href="mailto:ciieaimicommunity@gmail.com"
      style="color:cyan;">ciieaimicommunity@gmail.com</a></li>
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
<p>Follow our LinkedIn: <a href="https://www.linkedin.com/company/ciie-aiml-community/" target="_blank"
    style="color:cyan;">CIIE AIML Community</a></p>
""", path="/info")

@app.get("/team", response_class=HTMLResponse)
async def team():
    return render("""
<h2>Our Team</h2>
<div class="animated-team">
  <h3>Faculty Mentors</h3>
  <div class="team" style="display:flex; justify-content:center; flex-wrap:wrap; gap:2rem;">
    <div class="card faculty" style="width:250px; height:250px; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center;">
      <div class="card-content" style="margin-bottom:0.5rem;">
        <strong>Ahmed Sir</strong><br>Faculty Mentor
      </div>
      <img src="/static/images/Ahmad sir.png" alt="Ahmed Sir" style="width:120px; height:120px; border-radius:50%; object-fit:cover; margin-top:0.5rem; margin-bottom:0.6rem; border:3px solid gold;">
    </div>
  </div>
  <h3>Core Members</h3>
  <div class="team" style="display:flex; flex-wrap:wrap; gap:2rem; justify-content:center;">
    <div class="card" style="width:250px; height:250px; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center;">
      <div class="card-content" style="display:flex; flex-direction:column; align-items:center;">
        <div style="margin-bottom:0.7rem;">
          <strong>Arpita</strong><br>Web Dev Lead
        </div>
        <img src="/static/images/arpita.png" alt="Arpita" style="width:120px; height:120px; border-radius:50%; object-fit:cover; margin-top:0.5rem; margin-bottom:0.6rem;">
      </div>
      <div class="card-social" style="text-align:center;">
        <a href="#" target="_blank"><i class="fab fa-linkedin"></i></a>
        <a href="#" target="_blank"><i class="fab fa-github"></i></a>
      </div>
    </div>
    <div class="card" style="width:250px; height:250px; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center;">
      <div class="card-content" style="display:flex; flex-direction:column; align-items:center;">
        <div style="margin-bottom:0.7rem;">
          <strong>Shubham</strong><br>App Dev Lead
        </div>
        <img src="/static/images/shubham.png" alt="Shubham" style="width:120px; height:120px; border-radius:50%; object-fit:cover; margin-top:0.5rem; margin-bottom:0.6rem;">
      </div>
      <div class="card-social" style="text-align:center;">
        <a href="#" target="_blank"><i class="fab fa-linkedin"></i></a>
        <a href="#" target="_blank"><i class="fab fa-github"></i></a>
      </div>
    </div>
    <div class="card" style="width:250px; height:250px; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center;">
      <div class="card-content" style="display:flex; flex-direction:column; align-items:center;">
        <div style="margin-bottom:0.7rem;">
          <strong>Arshiya</strong><br>Research Head
        </div>
        <img src="/static/images/arshiya.png" alt="Arshiya" style="width:120px; height:120px; border-radius:50%; object-fit:cover; margin-top:0.5rem; margin-bottom:0.6rem;">
      </div>
      <div class="card-social" style="text-align:center;">
        <a href="#" target="_blank"><i class="fab fa-linkedin"></i></a>
        <a href="#" target="_blank"><i class="fab fa-github"></i></a>
      </div>
    </div>
    <div class="card" style="width:250px; height:250px; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center;">
      <div class="card-content" style="display:flex; flex-direction:column; align-items:center;">
        <div style="margin-bottom:0.7rem;">
          <strong>Rajveer</strong><br>Workshop Lead
        </div>
        <img src="/static/images/rajveer.png" alt="Rajveer" style="width:120px; height:120px; border-radius:50%; object-fit:cover; margin-top:0.5rem; margin-bottom:0.6rem;">
      </div>
      <div class="card-social" style="text-align:center;">
        <a href="#" target="_blank"><i class="fab fa-linkedin"></i></a>
        <a href="#" target="_blank"><i class="fab fa-github"></i></a>
      </div>
    </div>
    <div class="card" style="width:250px; height:250px; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center;">
      <div class="card-content" style="display:flex; flex-direction:column; align-items:center;">
        <div style="margin-bottom:0.7rem;">
          <strong>Ishita</strong><br>Data Science & Design
        </div>
        <img src="/static/images/ishita.png" alt="Ishita" style="width:120px; height:120px; border-radius:50%; object-fit:cover; margin-top:0.5rem; margin-bottom:0.6rem;">
      </div>
      <div class="card-social" style="text-align:center;">
        <a href="#" target="_blank"><i class="fab fa-linkedin"></i></a>
        <a href="#" target="_blank"><i class="fab fa-github"></i></a>
      </div>
    </div>
    <div class="card" style="width:250px; height:250px; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center;">
      <div class="card-content" style="display:flex; flex-direction:column; align-items:center;">
        <div style="margin-bottom:0.7rem;">
          <strong>Trisha</strong><br>Marketing Lead
        </div>
        <img src="/static/images/trisha.png" alt="Trisha" style="width:120px; height:120px; border-radius:50%; object-fit:cover; margin-top:0.5rem; margin-bottom:0.6rem;">
      </div>
      <div class="card-social" style="text-align:center;">
        <a href="#" target="_blank"><i class="fab fa-linkedin"></i></a>
        <a href="#" target="_blank"><i class="fab fa-github"></i></a>
      </div>
    </div>
    <div class="card" style="width:250px; height:250px; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center;">
      <div class="card-content" style="display:flex; flex-direction:column; align-items:center;">
        <div style="margin-bottom:0.7rem;">
          <strong>Nitan</strong><br>Project Lead
        </div>
        <img src="/static/images/nitan.png" alt="Nitan" style="width:120px; height:120px; border-radius:50%; object-fit:cover; margin-top:0.5rem; margin-bottom:0.6rem;">
      </div>
      <div class="card-social" style="text-align:center;">
        <a href="#" target="_blank"><i class="fab fa-linkedin"></i></a>
        <a href="#" target="_blank"><i class="fab fa-github"></i></a>
      </div>
    </div>
    <div class="card" style="width:250px; height:250px; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center;">
      <div class="card-content" style="display:flex; flex-direction:column; align-items:center;">
        <div style="margin-bottom:0.7rem;">
          <strong>Prateek</strong><br>AIML Lead
        </div>
        <img src="/static/images/Partik (1).png" alt="Prateek" style="width:120px; height:120px; border-radius:50%; object-fit:cover; margin-top:0.5rem; margin-bottom:0.6rem;">
      </div>
      <div class="card-social" style="text-align:center;">
        <a href="#" target="_blank"><i class="fab fa-linkedin"></i></a>
        <a href="#" target="_blank"><i class="fab fa-github"></i></a>
      </div>
    </div>
  </div>
</div>
<style>
.animated-team {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
  margin-top: 1rem;
}
.animated-team .card {
  background: rgba(0, 255, 255, 0.13);
  box-shadow: 0 0 6px rgba(0,255,255,0.18);
  border-radius: 12px;
  font-weight: bold;
  min-width: 120px;
  text-align: center;
  cursor: pointer;
  transition: transform 0.3s, background 0.3s, box-shadow 0.3s;
  user-select: none;
  position: relative;
  /* width and height are set inline for each card for square shape */
  /* display:flex, flex-direction:column, align-items:center, justify-content:center are set inline */
}
.animated-team .card:hover {
  background: rgba(0, 255, 255, 0.22);
  transform: translateY(-5px) scale(1.05);
  box-shadow: 0 0 18px rgba(0,255,255,0.37);
}
</style>
<script>
const teamCards = document.querySelectorAll('.animated-team .card');
setInterval(() => {
  teamCards.forEach((card, i) => {
    const y = Math.sin(Date.now() / 1400 + i) * 12;
    card.style.transform = `translateY(${y}px)`;
  });
}, 16);
</script>
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


# -------------------- Event Registration -------------------- #
@app.get("/events", response_class=HTMLResponse)
async def events_page():
    return render("""
<h2>Upcoming Events</h2>
<style>
.animated-events {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  justify-content: center;
  margin-top: 2rem;
}
.animated-events .card {
  transition: transform 0.3s ease;
}
</style>
<div class="animated-events">
  <div class="card">
    <div class="card-content">
      <strong>AI Hackathon 2025</strong><br>
      Date: November 15-17, 2025<br>
      48-hour coding challenge
    </div>
  </div>
  <div class="card">
    <div class="card-content">
      <strong>Machine Learning Workshop</strong><br>
      Date: November 25, 2025<br>
      Hands-on ML training
    </div>
  </div>
  <div class="card">
    <div class="card-content">
      <strong>Data Science Bootcamp</strong><br>
      Date: December 5-7, 2025<br>
      3-day intensive program
    </div>
  </div>
  <div class="card">
    <div class="card-content">
      <strong>AI Innovation Summit</strong><br>
      Date: December 15, 2025<br>
      Industry experts & networking
    </div>
  </div>
</div>
<script>
const eventCards = document.querySelectorAll('.animated-events .card');
setInterval(() => {
  eventCards.forEach((card, i) => {
    const y = Math.sin(Date.now() / 1500 + i) * 10;
    card.style.transform = `translateY(${y}px)`;
  });
}, 16);
</script>
<div style="text-align:center; margin-top:2rem;">
  <button onclick="openRegistrationModal()"
    style="padding:1rem 2rem; font-size:1.1rem; background:linear-gradient(135deg, #00ffff, #0080ff); border:none; border-radius:8px; color:white; font-weight:bold; cursor:pointer; transition:all 0.3s ease; box-shadow:0 0 20px rgba(0,255,255,0.4);">
    <i class="fas fa-calendar-check" style="margin-right:0.5rem;"></i>Register for Event
  </button>
</div>
""", path="/events")

@app.post("/register-event", response_class=HTMLResponse)
async def register_event(
    fullname: str = Form(...),
    course: str = Form(...),
    year_semester: str = Form(...),
    phone: str = Form(...),
    email: str = Form(None),
    event: str = Form(...)
):
    # Store registration
    registration = {
        "fullname": fullname,
        "course": course,
        "year_semester": year_semester,
        "phone": phone,
        "email": email,
        "event": event,
        "timestamp": datetime.now().isoformat()
    }
    event_registrations.append(registration)

    return render(f"""
    <div style="text-align:center; padding:2rem;">
      <div style="font-size:4rem; margin-bottom:1rem;"></div>
      <h2 style="color:#00ffff; margin-bottom:1rem;">Thank You for Registering!</h2>
      <p style="font-size:1.2rem; margin-bottom:1rem;">
        <strong>{fullname}</strong>, your registration for <strong>{event}</strong> has been confirmed!
      </p>
      <p style="color:#00ffff;">You will receive event details soon on your registered contact.</p>
      <div style="margin-top:2rem;">
        <a href="/events"
          style="display:inline-block; padding:0.8rem 2rem; background:#ff9800; color:white; text-decoration:none; border-radius:6px; font-weight:bold; transition:all 0.3s ease;">
          View All Events
        </a>
      </div>
    </div>
    """, path="/events")

# View registrations endpoint (optional - for admin)
@app.get("/view-registrations", response_class=HTMLResponse)
async def view_registrations():
    if not event_registrations:
        registrations_html = "<p>No registrations yet.</p>"
    else:
        registrations_html = "<div class='team'>"
        for reg in event_registrations:
            registrations_html += f"""
            <div class="card" style="text-align:left;">
                <strong>{reg['fullname']}</strong><br>
                Event: {reg['event']}<br>
                Course: {reg['course']}<br>
                Year: {reg['year_semester']}<br>
                Phone: {reg['phone']}<br>
                Email: {reg.get('email', 'Not provided')}<br>
                <small>Registered: {reg['timestamp']}</small>
            </div>
            """
        registrations_html += "</div>"

    return render(f"""
    <h2>Event Registrations</h2>
    {registrations_html}
    """, path="/view-registrations")