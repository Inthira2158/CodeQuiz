# ⚡ CodeQuiz – Programming Quiz Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.x-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![Prism.js](https://img.shields.io/badge/Prism.js-Syntax_Highlighting-2B2B2B?logo=javascript&logoColor=white)](https://prismjs.com/)
[![Chart.js](https://img.shields.io/badge/Chart.js-4.x-FF6384?logo=chartdotjs&logoColor=white)](https://www.chartjs.org/)

**CodeQuiz** is a full-stack, developer-focused programming quiz and assessment platform. Designed to sharpen engineering problem-solving and technical interview readiness across **Python, Java, SQL, HTML, CSS, and JavaScript**.

---

## 🌟 Key Features

### 1. 🎯 Topic-Based Programming Quizzes
- **6 Core Supported Technologies**:
  - 🐍 **Python**: List comprehensions, decorators, generators, OOP, mutable defaults, slicing.
  - ☕ **Java**: OOP polymorphism, functional interfaces, Streams, memory models, `volatile`, concurrency.
  - 🗄️ **SQL**: Relational `JOIN`s, `GROUP BY`, `HAVING`, window functions, ACID properties, subqueries.
  - 🌐 **HTML**: HTML5 semantic markup, `<canvas>` vs `<svg>`, security headers, accessibility (`<label for>`).
  - 🎨 **CSS**: Modern Flexbox, CSS Grid `repeat(auto-fit, minmax(...))`, box model, specificity, `position: sticky`.
  - ⚡ **JavaScript**: Event loop microtasks/macrotasks, closures, arrow `this`, `Promise.allSettled`, strict equality.
- **Difficulty Settings**: Beginner, Intermediate, Advanced, or Mixed.
- **Flexible Lengths**: 5, 10, or 15 questions per session.
- **Syntax Highlighting**: Real-time syntax highlighting for code snippets powered by Prism.js.

### 2. ⏱️ Precision Countdown Timer & Automatic Scoring
- **Multiple Timer Modes**:
  - **Per-Question Countdown**: Configurable 30-second timer per question with sound ticks and auto-advance.
  - **Total Session Countdown**: Timed session timer with automatic instant submission upon expiry.
  - **Practice Mode**: Untimed self-paced study mode with instant evaluation.
- **Urgency Alerts**: Visual alert transitions (Green ➔ Amber pulse at 10s ➔ Red warning at 5s) and Web Audio synthesizer tick cues.
- **Automated Instant Scoring**:
  - Accuracy percentage calculation.
  - Points algorithm awarding **+20 points** per correct answer plus **speed bonuses** for quick solutions.
  - Confetti celebration animation on achieving 80%+ scores.

### 3. 🏆 Global & Topic Leaderboards
- **Hall of Fame Podium**: Displays 1st (Gold 🥇), 2nd (Silver 🥈), and 3rd (Bronze 🥉) rank champions with customized badges.
- **Topic-Specific Rankings**: Filter leaderboards dynamically by Python, Java, SQL, HTML, CSS, or JavaScript.
- **Personal Rank Highlighting**: Instantly showcases the active user's standing and points.

### 4. 📊 Progress Tracking by Topic
- **Skills Mastery Radar Chart**: Visual Chart.js radar plot illustrating technical strengths and balance across all 6 topics.
- **Mastery Hierarchy**: Dynamic classification (`Novice` ➔ `Apprentice` ➔ `Skilled` ➔ `Master` ➔ `Grandmaster`).
- **Comprehensive Quiz History**: Chronological log of past attempts with score percentages, time taken, and "Review" links.
- **Milestones & Achievements**: Unlockable badges (*First Steps*, *Flawless Victory*, *Speed Demon*, *The Polyglot*, *Grandmaster*).

### 5. 🔍 In-Depth Question Review & Explanations
- Every submitted quiz delivers an exhaustive question-by-question debrief.
- Side-by-side indicator comparing **Your Selected Answer** against the **Correct Answer**.
- Filter review items by: *All*, *Correct*, *Wrong*, or *Skipped*.
- Detailed **Technical Explanation** for each question explaining the exact reasoning behind the solution.

### 6. ✍️ Community Question Creation
- User-friendly authoring interface to contribute new quiz questions.
- Customizable code snippets, multiple-choice options, correct option selector, and markdown-friendly technical explanations.

---

## 🛠️ Tech Stack & Architecture

- **Backend Framework**: Python 3.10+ & Flask 3.x
- **Database**: SQLite3 (`codequiz.db`) with Foreign Keys, indexed lookups, and auto-aggregations.
- **Frontend UI**: Bootstrap 5.3 Dark Mode, FontAwesome 6, Custom responsive CSS.
- **Code Highlighting**: Prism.js Tomorrow Night theme (Python, Java, SQL, JS, CSS).
- **Interactive Charts**: Chart.js 4.x (Radar charts and progress bars).
- **Celebration Effects**: Canvas Confetti.
- **Audio Feedback**: Self-contained HTML5 Web Audio API synthesizer tones (zero external audio asset dependencies).

---

## 📁 Project Structure

```
Project/
├── app.py                  # Main Flask routes, controllers, and error handlers
├── config.py               # Application configuration and database settings
├── database.py             # Database access layer, score calculation, mastery logic
├── schema.sql              # Relational database schema definitions
├── seed_data.py            # Question bank (72+ rich questions) and leaderboard seed
├── test_app.py             # Automated unit and integration test suite
├── requirements.txt        # Python package dependencies
├── run.bat                 # One-click Windows startup script
├── render.yaml             # Render cloud deployment specification
├── static/
│   ├── css/
│   │   └── style.css       # Custom modern dark developer UI stylesheet
│   └── js/
│       ├── main.js         # General UI helpers and alert dismissals
│       └── quiz.js         # Client-side quiz engine, timer, and keyboard shortcuts
└── templates/
    ├── base.html           # Base layout with navbar, footer, and notifications
    ├── index.html          # Landing page with topic cards and leaderboard preview
    ├── leaderboard.html    # Global and topic-filtered rankings table
    ├── progress.html       # Topic mastery dashboard and Radar chart
    ├── 404.html / 500.html # Custom error pages
    ├── auth/
    │   ├── login.html      # User authentication login
    │   └── register.html   # User registration
    └── quiz/
        ├── setup.html      # Quiz configuration modal
        ├── play.html       # Interactive timed quiz player
        ├── result.html     # Results breakdown, confetti & question review
        └── create.html     # Question authoring form
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.10 or higher installed.

### 2. Setup & Database Seeding
Open your terminal in the project directory:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Seed database with topics, 72+ programming questions, and leaderboards
python seed_data.py
```

### 3. Start the Server
```bash
python app.py
```

Or on Windows, simply double-click `run.bat`!

Visit **[http://127.0.0.1:5000](http://127.0.0.1:5000)** in your browser.

---

## 🧪 Running Automated Tests

Run the complete test suite covering database models, question retrieval, quiz scoring, leaderboard sorting, and question creation:

```bash
python test_app.py
```

---

## 👤 Demo Login Credentials

For quick evaluation, pre-seeded accounts are available:
- **Username**: `AlexDev` | **Password**: `password123`
- **Username**: `Sara_Coder` | **Password**: `password123`
- *Or click "Quick Play (Guest)" on the home page to jump straight into any quiz without credentials!*
