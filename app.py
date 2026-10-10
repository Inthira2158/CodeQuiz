"""
app.py - Main Flask Application for CodeQuiz: Programming Quiz Platform
"""

import os
import json
from flask import (
    Flask, render_template, request, redirect, url_for,
    flash, session, g, jsonify, abort
)
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
import database as db

app = Flask(__name__)
app.config.from_object(Config)

# Auto-seed database if it doesn't exist (crucial for zero-config cloud deployments)
if not os.path.exists(Config.DATABASE):
    try:
        from seed_data import seed_database
        print("Database not found on startup. Auto-seeding initial database...")
        seed_database()
        print("Auto-seeding complete.")
    except Exception as _e:
        print(f"Auto-seed exception: {_e}")

# Register teardown function for database
app.teardown_appcontext(db.close_db)


@app.before_request
def load_logged_in_user():
    """Loads the logged-in user into flask.g before every request."""
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = db.get_user_by_id(user_id)


@app.context_processor
def inject_global_data():
    """Injects common data like topics and user context into all templates."""
    try:
        all_topics = db.get_all_topics()
    except Exception:
        all_topics = []
    return {
        'current_user': g.user,
        'global_topics': all_topics,
        'site_title': 'CodeQuiz'
    }


def login_required(view):
    """Decorator to require login for certain views."""
    import functools
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash('Please log in or create an account to access this page.', 'warning')
            return redirect(url_for('login', next=request.url))
        return view(**kwargs)
    return wrapped_view


# ==========================================
# PUBLIC & HOME ROUTES
# ==========================================

@app.route('/')
def index():
    """Landing page featuring topic selection cards, top rankings, and overview stats."""
    topics = db.get_all_topics()
    top_users = db.get_global_leaderboard(limit=5)
    
    # Platform statistics
    total_quizzes = db.query_db("SELECT COUNT(*) AS cnt FROM quiz_attempts", one=True)['cnt']
    total_questions = db.query_db("SELECT COUNT(*) AS cnt FROM questions", one=True)['cnt']
    total_users = db.query_db("SELECT COUNT(*) AS cnt FROM users", one=True)['cnt']
    
    return render_template('index.html',
                           topics=topics,
                           top_users=top_users,
                           total_quizzes=total_quizzes,
                           total_questions=total_questions,
                           total_users=total_users)


# ==========================================
# AUTHENTICATION ROUTES
# ==========================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        username_or_email = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        # Search by username or email
        user = db.get_user_by_username(username_or_email)
        if not user:
            user = db.get_user_by_email(username_or_email)
            
        if user and check_password_hash(user['password_hash'], password):
            session.clear()
            session['user_id'] = user['id']
            flash(f"Welcome back, {user['username']}! Ready for your next coding challenge?", 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('progress'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')
            
    return render_template('auth/login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if g.user:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        avatar = request.form.get('avatar', 'avatar-1')
        bio = request.form.get('bio', 'Aspiring developer & quiz enthusiast')
        
        # Validations
        if not username or len(username) < 3:
            flash('Username must be at least 3 characters long.', 'danger')
        elif not email or '@' not in email:
            flash('Please provide a valid email address.', 'danger')
        elif len(password) < 6:
            flash('Password must be at least 6 characters long.', 'danger')
        elif password != confirm_password:
            flash('Passwords do not match.', 'danger')
        elif db.get_user_by_username(username):
            flash('Username is already taken. Please choose another one.', 'danger')
        elif db.get_user_by_email(email):
            flash('Email is already registered. Please log in.', 'danger')
        else:
            password_hash = generate_password_hash(password)
            user_id = db.create_user(username, email, password_hash, avatar, bio)
            session.clear()
            session['user_id'] = user_id
            flash('Registration successful! Welcome to CodeQuiz!', 'success')
            return redirect(url_for('progress'))
            
    return render_template('auth/register.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


@app.route('/guest-login', methods=['POST'])
def guest_login():
    """Allows rapid play without password creation by generating/resuming a guest session."""
    guest_name = request.form.get('guest_name', '').strip()
    if not guest_name:
        guest_name = 'Coder_' + os.urandom(2).hex()
    
    # Check if exists or create guest user
    existing = db.get_user_by_username(guest_name)
    if not existing:
        dummy_hash = generate_password_hash('guest1234')
        user_id = db.create_user(guest_name, f"{guest_name.lower()}@codequiz.local", dummy_hash, avatar='avatar-guest', bio='Guest Participant')
    else:
        user_id = existing['id']
        
    session.clear()
    session['user_id'] = user_id
    flash(f"Welcome, {guest_name}! You are playing in quick session mode.", 'info')
    
    redirect_topic = request.form.get('redirect_topic')
    if redirect_topic:
        return redirect(url_for('quiz_setup', topic_slug=redirect_topic))
    return redirect(url_for('index'))


# ==========================================
# QUIZ SETUP & EXECUTION ENGINE
# ==========================================

@app.route('/quiz/setup/<topic_slug>')
def quiz_setup(topic_slug):
    """Customization screen before starting a quiz: pick difficulty, timer mode, question count."""
    topic = db.get_topic_by_slug(topic_slug)
    if not topic:
        flash('Requested topic not found.', 'danger')
        return redirect(url_for('index'))
        
    # User's stats for this topic if logged in
    user_stats = None
    if g.user:
        user_stats = db.query_db("""
            SELECT * FROM user_topic_stats 
            WHERE user_id = ? AND topic_slug = ?
        """, (g.user['id'], topic_slug), one=True)
        
    return render_template('quiz/setup.html', topic=topic, user_stats=user_stats)


@app.route('/quiz/play/<topic_slug>', methods=['GET', 'POST'])
def quiz_play(topic_slug):
    """Interactive quiz playing interface with timer and automatic scoring."""
    topic = db.get_topic_by_slug(topic_slug)
    if not topic:
        flash('Topic not found.', 'danger')
        return redirect(url_for('index'))
        
    difficulty = request.args.get('difficulty', 'Mixed')
    question_count = int(request.args.get('count', 10))
    timer_mode = request.args.get('timer_mode', 'per_question') # 'per_question', 'total', 'practice'
    
    # Fetch questions
    questions_rows = db.get_questions_for_quiz(topic_slug, difficulty=difficulty, limit=question_count)
    if not questions_rows:
        flash('No questions currently available for this topic and difficulty.', 'warning')
        return redirect(url_for('quiz_setup', topic_slug=topic_slug))
        
    # Serialize questions for client-side state without giving away correct answers
    questions_data = []
    for q in questions_rows:
        questions_data.append({
            'id': q['id'],
            'difficulty': q['difficulty'],
            'question_text': q['question_text'],
            'code_snippet': q['code_snippet'] or '',
            'code_lang': q['code_lang'] or topic['code_lang'],
            'option_a': q['option_a'],
            'option_b': q['option_b'],
            'option_c': q['option_c'],
            'option_d': q['option_d'],
            'time_limit_sec': q['time_limit_sec'] or 30
        })

    total_time_limit = sum(q['time_limit_sec'] for q in questions_data) if timer_mode == 'total' else 30

    return render_template('quiz/play.html',
                           topic=topic,
                           difficulty=difficulty,
                           timer_mode=timer_mode,
                           total_time_limit=total_time_limit,
                           questions_json=json.dumps(questions_data),
                           question_count=len(questions_data))


@app.route('/quiz/submit', methods=['POST'])
def quiz_submit():
    """Processes submitted quiz answers, calculates automatic score and updates user progress."""
    # Ensure user exists (or create guest on the fly)
    user_id = session.get('user_id')
    if not user_id:
        # Create quick guest
        guest_name = 'Guest_' + os.urandom(2).hex()
        dummy_hash = generate_password_hash('guest1234')
        user_id = db.create_user(guest_name, f"{guest_name.lower()}@codequiz.local", dummy_hash, avatar='avatar-guest')
        session['user_id'] = user_id
        
    # Parse payload (form or JSON)
    if request.is_json:
        data = request.get_json()
    else:
        try:
            data = json.loads(request.form.get('quiz_submission_payload', '{}'))
        except Exception:
            data = request.form.to_dict()

    topic_slug = data.get('topic_slug')
    difficulty = data.get('difficulty', 'Mixed')
    time_taken_sec = int(data.get('total_time_spent', 0))
    answers_map = data.get('answers', {}) # {question_id: {'selected': 'A', 'time': 12}}
    
    if not topic_slug or not answers_map:
        flash('Invalid quiz submission data.', 'danger')
        return redirect(url_for('index'))

    # Verify answers against database
    q_ids = list(map(int, answers_map.keys()))
    placeholders = ','.join(['?'] * len(q_ids))
    questions_in_db = db.query_db(f"SELECT * FROM questions WHERE id IN ({placeholders})", q_ids)
    
    q_dict = {q['id']: q for q in questions_in_db}
    
    total_questions = len(q_ids)
    correct_count = 0
    wrong_count = 0
    skipped_count = 0
    detailed_answers = []

    for q_id_str, ans_data in answers_map.items():
        q_id = int(q_id_str)
        q = q_dict.get(q_id)
        if not q:
            continue
            
        selected_option = ans_data.get('selected')
        time_spent = int(ans_data.get('time', 0))
        
        if not selected_option:
            is_correct = False
            skipped_count += 1
        elif selected_option.upper() == q['correct_option'].upper():
            is_correct = True
            correct_count += 1
        else:
            is_correct = False
            wrong_count += 1
            
        detailed_answers.append({
            'question_id': q_id,
            'selected_option': selected_option.upper() if selected_option else None,
            'is_correct': is_correct,
            'time_spent_sec': time_spent
        })

    # Calculate score percentage & point algorithm
    score_percentage = round((correct_count / total_questions * 100.0), 1) if total_questions > 0 else 0.0
    
    # Points calculation:
    # 20 points per correct answer + speed bonus (up to 10 extra points per correct question if answered fast)
    base_points = correct_count * 20
    speed_bonus = max(0, int((total_questions * 25 - time_taken_sec) * 0.5)) if correct_count > 0 else 0
    points_earned = base_points + speed_bonus

    # Save to database
    attempt_id = db.save_quiz_attempt(
        user_id=user_id,
        topic_slug=topic_slug,
        difficulty=difficulty,
        total_questions=total_questions,
        correct_answers=correct_count,
        wrong_answers=wrong_count,
        skipped_answers=skipped_count,
        score_percentage=score_percentage,
        points_earned=points_earned,
        time_taken_sec=time_taken_sec,
        detailed_answers=detailed_answers
    )

    # Check achievements
    attempt_summary = {
        'score_percentage': score_percentage,
        'time_taken_sec': time_taken_sec,
        'total_questions': total_questions,
        'points_earned': points_earned
    }
    new_achievements = db.check_and_unlock_achievements(user_id, attempt_summary)
    if new_achievements:
        session['new_achievements'] = new_achievements

    if request.is_json:
        return jsonify({
            'status': 'success',
            'redirect_url': url_for('quiz_result', attempt_id=attempt_id)
        })

    return redirect(url_for('quiz_result', attempt_id=attempt_id))


@app.route('/quiz/result/<int:attempt_id>')
def quiz_result(attempt_id):
    """Detailed score report, question review with explanations, and ranking impact."""
    attempt = db.get_quiz_attempt(attempt_id)
    if not attempt:
        flash('Quiz attempt record not found.', 'danger')
        return redirect(url_for('index'))
        
    detailed_answers = db.get_attempt_answers_detailed(attempt_id)
    new_achievements = session.pop('new_achievements', [])
    
    # User's ranking
    user_rank = db.get_user_rank(attempt['user_id'])
    
    return render_template('quiz/result.html',
                           attempt=attempt,
                           answers=detailed_answers,
                           new_achievements=new_achievements,
                           user_rank=user_rank)


# ==========================================
# LEADERBOARD & RANKINGS
# ==========================================

@app.route('/leaderboard')
def leaderboard():
    """Displays global and topic-specific leaderboards with rankings."""
    selected_topic = request.args.get('topic', 'all')
    topics = db.get_all_topics()
    
    if selected_topic == 'all':
        rankings = db.get_global_leaderboard(limit=50)
        current_topic_name = 'Global (All Topics)'
    else:
        topic_obj = db.get_topic_by_slug(selected_topic)
        if topic_obj:
            rankings = db.get_topic_leaderboard(selected_topic, limit=50)
            current_topic_name = topic_obj['name']
        else:
            rankings = db.get_global_leaderboard(limit=50)
            current_topic_name = 'Global'
            selected_topic = 'all'

    # Current user standing
    my_rank = None
    if g.user:
        my_rank = db.get_user_rank(g.user['id'])

    return render_template('leaderboard.html',
                           rankings=rankings,
                           topics=topics,
                           selected_topic=selected_topic,
                           current_topic_name=current_topic_name,
                           my_rank=my_rank)


# ==========================================
# PROGRESS TRACKING & TOPIC MASTERY
# ==========================================

@app.route('/progress')
@login_required
def progress():
    """Personal progress tracking dashboard broken down by topic."""
    user_id = g.user['id']
    topic_progress = db.get_user_topic_progress(user_id)
    summary = db.get_user_overall_summary(user_id)
    history = db.get_user_quiz_history(user_id, limit=10)
    achievements = db.get_user_achievements(user_id)
    user_rank = db.get_user_rank(user_id)

    # Prepare data for Radar Chart
    radar_labels = [tp['name'] for tp in topic_progress]
    radar_scores = [tp['best_score'] for tp in topic_progress]
    radar_accuracy = [tp['accuracy_pct'] for tp in topic_progress]

    return render_template('progress.html',
                           topic_progress=topic_progress,
                           summary=summary,
                           history=history,
                           achievements=achievements,
                           user_rank=user_rank,
                           radar_labels=json.dumps(radar_labels),
                           radar_scores=json.dumps(radar_scores),
                           radar_accuracy=json.dumps(radar_accuracy))


# ==========================================
# CREATE QUIZ / QUESTION MANAGEMENT
# ==========================================

@app.route('/quiz/create', methods=['GET', 'POST'])
@login_required
def create_question():
    """Allows users / educators to create new programming quiz questions."""
    topics = db.get_all_topics()
    
    if request.method == 'POST':
        topic_slug = request.form.get('topic_slug')
        difficulty = request.form.get('difficulty', 'Intermediate')
        question_text = request.form.get('question_text', '').strip()
        code_snippet = request.form.get('code_snippet', '').strip()
        code_lang = request.form.get('code_lang', topic_slug)
        option_a = request.form.get('option_a', '').strip()
        option_b = request.form.get('option_b', '').strip()
        option_c = request.form.get('option_c', '').strip()
        option_d = request.form.get('option_d', '').strip()
        correct_option = request.form.get('correct_option', '').strip().upper()
        explanation = request.form.get('explanation', '').strip()
        time_limit_sec = int(request.form.get('time_limit_sec', 30))
        
        # Validations
        if not (topic_slug and question_text and option_a and option_b and option_c and option_d and correct_option and explanation):
            flash('Please fill in all mandatory question fields.', 'danger')
        elif correct_option not in ['A', 'B', 'C', 'D']:
            flash('Correct option must be one of A, B, C, or D.', 'danger')
        else:
            db.create_question(
                topic_slug=topic_slug,
                difficulty=difficulty,
                question_text=question_text,
                code_snippet=code_snippet,
                code_lang=code_lang,
                option_a=option_a,
                option_b=option_b,
                option_c=option_c,
                option_d=option_d,
                correct_option=correct_option,
                explanation=explanation,
                time_limit_sec=time_limit_sec,
                created_by=g.user['id']
            )
            flash('Question created successfully and added to the quiz bank!', 'success')
            return redirect(url_for('quiz_setup', topic_slug=topic_slug))
            
    return render_template('quiz/create.html', topics=topics)


# ==========================================
# API DATA ENDPOINTS
# ==========================================

@app.route('/api/leaderboard')
def api_leaderboard():
    topic = request.args.get('topic', 'all')
    if topic == 'all':
        data = db.get_global_leaderboard(limit=25)
    else:
        data = db.get_topic_leaderboard(topic, limit=25)
    return jsonify([dict(row) for row in data])


@app.route('/api/user/progress')
def api_user_progress():
    if not g.user:
        return jsonify({'error': 'Unauthorized'}), 401
    progress_data = db.get_user_topic_progress(g.user['id'])
    return jsonify([dict(row) for row in progress_data])


# ==========================================
# ERROR HANDLERS
# ==========================================

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    # Run development server
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
