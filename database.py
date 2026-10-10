"""
database.py - Database access layer for CodeQuiz platform
"""

import sqlite3
import os
from flask import g
from config import Config

def get_db():
    """Returns a database connection attached to the Flask request context."""
    if 'db' not in g:
        g.db = sqlite3.connect(Config.DATABASE)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON;")
    return g.db

def close_db(e=None):
    """Closes the database connection at the end of the request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    """Helper to query the database and fetch rows as dictionaries."""
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def execute_db(query, args=(), commit=True):
    """Helper to execute an INSERT/UPDATE/DELETE statement."""
    db = get_db()
    cur = db.execute(query, args)
    if commit:
        db.commit()
    lastrowid = cur.lastrowid
    cur.close()
    return lastrowid


# ==========================================
# USER OPERATIONS
# ==========================================

def get_user_by_id(user_id):
    return query_db("SELECT * FROM users WHERE id = ?", (user_id,), one=True)

def get_user_by_username(username):
    return query_db("SELECT * FROM users WHERE LOWER(username) = LOWER(?)", (username,), one=True)

def get_user_by_email(email):
    return query_db("SELECT * FROM users WHERE LOWER(email) = LOWER(?)", (email,), one=True)

def create_user(username, email, password_hash, avatar='avatar-1', bio='Code enthusiast & learner'):
    return execute_db("""
        INSERT INTO users (username, email, password_hash, avatar, bio)
        VALUES (?, ?, ?, ?, ?)
    """, (username, email, password_hash, avatar, bio))


# ==========================================
# TOPICS & QUESTIONS
# ==========================================

def get_all_topics():
    return query_db("""
        SELECT t.*, 
               (SELECT COUNT(*) FROM questions q WHERE q.topic_slug = t.slug) AS question_count,
               (SELECT COUNT(*) FROM quiz_attempts a WHERE a.topic_slug = t.slug) AS total_plays
        FROM topics t
        ORDER BY t.name ASC
    """)

def get_topic_by_slug(slug):
    return query_db("""
        SELECT t.*, 
               (SELECT COUNT(*) FROM questions q WHERE q.topic_slug = t.slug) AS question_count,
               (SELECT COUNT(*) FROM quiz_attempts a WHERE a.topic_slug = t.slug) AS total_plays
        FROM topics t
        WHERE t.slug = ?
    """, (slug,), one=True)

def get_questions_for_quiz(topic_slug, difficulty=None, limit=10):
    """Fetches randomized questions for a quiz session based on topic and difficulty."""
    if difficulty and difficulty != 'Mixed':
        return query_db("""
            SELECT * FROM questions 
            WHERE topic_slug = ? AND difficulty = ?
            ORDER BY RANDOM()
            LIMIT ?
        """, (topic_slug, difficulty, limit))
    else:
        return query_db("""
            SELECT * FROM questions 
            WHERE topic_slug = ?
            ORDER BY RANDOM()
            LIMIT ?
        """, (topic_slug, limit))

def get_question_by_id(question_id):
    return query_db("SELECT * FROM questions WHERE id = ?", (question_id,), one=True)

def create_question(topic_slug, difficulty, question_text, code_snippet, code_lang,
                    option_a, option_b, option_c, option_d, correct_option, explanation,
                    time_limit_sec=30, created_by=None):
    return execute_db("""
        INSERT INTO questions (
            topic_slug, difficulty, question_text, code_snippet, code_lang,
            option_a, option_b, option_c, option_d, correct_option, explanation,
            time_limit_sec, created_by
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        topic_slug, difficulty, question_text, code_snippet, code_lang,
        option_a, option_b, option_c, option_d, correct_option, explanation,
        time_limit_sec, created_by
    ))


# ==========================================
# QUIZ ATTEMPTS & SCORING
# ==========================================

def save_quiz_attempt(user_id, topic_slug, difficulty, total_questions, correct_answers,
                      wrong_answers, skipped_answers, score_percentage=0.0, points_earned=0, time_taken_sec=0,
                      detailed_answers=None, score_pct=None):
    """
    Saves a completed quiz attempt, records individual question answers,
    updates user's overall points and user topic mastery stats.
    """
    if score_pct is not None and (score_percentage is None or score_percentage == 0.0):
        score_percentage = score_pct
    if detailed_answers is None:
        detailed_answers = []

    db = get_db()
    cursor = db.cursor()

    # 1. Insert quiz attempt
    cursor.execute("""
        INSERT INTO quiz_attempts (
            user_id, topic_slug, difficulty, total_questions, correct_answers,
            wrong_answers, skipped_answers, score_percentage, points_earned, time_taken_sec
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id, topic_slug, difficulty, total_questions, correct_answers,
        wrong_answers, skipped_answers, score_percentage, points_earned, time_taken_sec
    ))
    attempt_id = cursor.lastrowid

    # 2. Insert detailed answers
    for ans in detailed_answers:
        cursor.execute("""
            INSERT INTO attempt_answers (
                attempt_id, question_id, selected_option, is_correct, time_spent_sec
            ) VALUES (?, ?, ?, ?, ?)
        """, (
            attempt_id, ans['question_id'], ans.get('selected_option'),
            1 if ans.get('is_correct') else 0, ans.get('time_spent_sec', 0)
        ))

    # 3. Update User total_points
    cursor.execute("""
        UPDATE users SET total_points = total_points + ? WHERE id = ?
    """, (points_earned, user_id))

    # 4. Update or Insert user_topic_stats
    cursor.execute("""
        SELECT id, quizzes_taken, total_questions_attempted, total_correct, best_score, total_time_spent_sec
        FROM user_topic_stats WHERE user_id = ? AND topic_slug = ?
    """, (user_id, topic_slug))
    stat_row = cursor.fetchone()

    if stat_row:
        new_taken = stat_row['quizzes_taken'] + 1
        new_attempted = stat_row['total_questions_attempted'] + total_questions
        new_correct = stat_row['total_correct'] + correct_answers
        new_best = max(stat_row['best_score'], score_percentage)
        new_time = stat_row['total_time_spent_sec'] + time_taken_sec
        
        # Calculate mastery
        if new_best >= 95 and new_taken >= 3:
            mastery = 'Grandmaster'
        elif new_best >= 85:
            mastery = 'Master'
        elif new_best >= 70:
            mastery = 'Skilled'
        elif new_best >= 50:
            mastery = 'Apprentice'
        else:
            mastery = 'Novice'

        cursor.execute("""
            UPDATE user_topic_stats
            SET quizzes_taken = ?, total_questions_attempted = ?, total_correct = ?,
                best_score = ?, total_time_spent_sec = ?, mastery_level = ?, last_played = CURRENT_TIMESTAMP
            WHERE user_id = ? AND topic_slug = ?
        """, (new_taken, new_attempted, new_correct, new_best, new_time, mastery, user_id, topic_slug))
    else:
        mastery = 'Master' if score_percentage >= 90 else ('Skilled' if score_percentage >= 70 else ('Apprentice' if score_percentage >= 50 else 'Novice'))
        cursor.execute("""
            INSERT INTO user_topic_stats (
                user_id, topic_slug, quizzes_taken, total_questions_attempted,
                total_correct, best_score, total_time_spent_sec, mastery_level, last_played
            ) VALUES (?, ?, 1, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (user_id, topic_slug, total_questions, correct_answers, score_percentage, time_taken_sec, mastery))

    db.commit()
    return attempt_id

def get_quiz_attempt(attempt_id):
    return query_db("""
        SELECT a.*, u.username, u.avatar, t.name AS topic_name, t.icon AS topic_icon, t.color AS topic_color
        FROM quiz_attempts a
        JOIN users u ON a.user_id = u.id
        JOIN topics t ON a.topic_slug = t.slug
        WHERE a.id = ?
    """, (attempt_id,), one=True)

def get_attempt_answers_detailed(attempt_id):
    return query_db("""
        SELECT aa.*, q.question_text, q.code_snippet, q.code_lang,
               q.option_a, q.option_b, q.option_c, q.option_d,
               q.correct_option, q.explanation
        FROM attempt_answers aa
        JOIN questions q ON aa.question_id = q.id
        WHERE aa.attempt_id = ?
        ORDER BY aa.id ASC
    """, (attempt_id,))


# ==========================================
# LEADERBOARD & RANKINGS
# ==========================================

def get_global_leaderboard(limit=50):
    return query_db("""
        SELECT u.id, u.username, u.avatar, u.bio, u.total_points,
               COUNT(a.id) AS quizzes_completed,
               COALESCE(ROUND(AVG(a.score_percentage), 1), 0.0) AS avg_accuracy,
               COALESCE(MAX(a.score_percentage), 0.0) AS highest_score
        FROM users u
        LEFT JOIN quiz_attempts a ON u.id = a.user_id
        GROUP BY u.id
        ORDER BY u.total_points DESC, avg_accuracy DESC
        LIMIT ?
    """, (limit,))

def get_topic_leaderboard(topic_slug, limit=50):
    return query_db("""
        SELECT u.id, u.username, u.avatar,
               s.quizzes_taken, s.best_score, s.mastery_level,
               ROUND((s.total_correct * 100.0 / NULLIF(s.total_questions_attempted, 0)), 1) AS accuracy,
               SUM(a.points_earned) AS topic_points
        FROM user_topic_stats s
        JOIN users u ON s.user_id = u.id
        JOIN quiz_attempts a ON (a.user_id = u.id AND a.topic_slug = s.topic_slug)
        WHERE s.topic_slug = ?
        GROUP BY u.id, s.topic_slug
        ORDER BY s.best_score DESC, topic_points DESC, accuracy DESC
        LIMIT ?
    """, (topic_slug, limit))

def get_user_rank(user_id):
    """Calculates overall ranking position of a user."""
    row = query_db("""
        SELECT COUNT(*) + 1 AS rank
        FROM users
        WHERE total_points > (SELECT total_points FROM users WHERE id = ?)
    """, (user_id,), one=True)
    return row['rank'] if row else 1


# ==========================================
# PROGRESS TRACKING & ANALYTICS
# ==========================================

def get_user_topic_progress(user_id):
    """
    Returns progress metrics for every available topic for a user.
    Includes mastery level, accuracy %, best score, quizzes taken,
    and calculates percentage toward mastery.
    """
    return query_db("""
        SELECT t.slug, t.name, t.icon, t.color, t.gradient,
               COALESCE(s.quizzes_taken, 0) AS quizzes_taken,
               COALESCE(s.total_questions_attempted, 0) AS total_questions_attempted,
               COALESCE(s.total_correct, 0) AS total_correct,
               COALESCE(s.best_score, 0.0) AS best_score,
               COALESCE(s.total_time_spent_sec, 0) AS total_time_spent_sec,
               COALESCE(s.mastery_level, 'Not Started') AS mastery_level,
               CASE 
                   WHEN s.total_questions_attempted > 0 
                   THEN ROUND((s.total_correct * 100.0 / s.total_questions_attempted), 1)
                   ELSE 0.0
               END AS accuracy_pct
        FROM topics t
        LEFT JOIN user_topic_stats s ON t.slug = s.topic_slug AND s.user_id = ?
        ORDER BY t.name ASC
    """, (user_id,))

def get_user_quiz_history(user_id, limit=20):
    return query_db("""
        SELECT a.*, t.name AS topic_name, t.icon AS topic_icon, t.color AS topic_color
        FROM quiz_attempts a
        JOIN topics t ON a.topic_slug = t.slug
        WHERE a.user_id = ?
        ORDER BY a.completed_at DESC
        LIMIT ?
    """, (user_id, limit))

def get_user_overall_summary(user_id):
    return query_db("""
        SELECT 
            COUNT(id) AS total_quizzes,
            COALESCE(SUM(total_questions), 0) AS total_questions_answered,
            COALESCE(SUM(correct_answers), 0) AS total_correct,
            COALESCE(ROUND(AVG(score_percentage), 1), 0.0) AS overall_avg_score,
            COALESCE(MAX(score_percentage), 0.0) AS peak_score,
            COALESCE(SUM(time_taken_sec), 0) AS total_study_time_sec
        FROM quiz_attempts
        WHERE user_id = ?
    """, (user_id,), one=True)


# ==========================================
# ACHIEVEMENTS UNLOCKING ENGINE
# ==========================================

def get_user_achievements(user_id):
    return query_db("""
        SELECT a.*, 
               CASE WHEN ua.id IS NOT NULL THEN 1 ELSE 0 END AS is_unlocked,
               ua.unlocked_at
        FROM achievements a
        LEFT JOIN user_achievements ua ON a.id = ua.achievement_id AND ua.user_id = ?
        ORDER BY is_unlocked DESC, a.points ASC
    """, (user_id,))

def check_and_unlock_achievements(user_id, attempt_data):
    """
    Evaluates milestone rules and awards new achievements.
    Returns list of newly unlocked achievements.
    """
    db = get_db()
    cursor = db.cursor()
    newly_unlocked = []

    # Get already unlocked slugs
    existing = {row['slug'] for row in query_db("""
        SELECT a.slug FROM user_achievements ua
        JOIN achievements a ON ua.achievement_id = a.id
        WHERE ua.user_id = ?
    """, (user_id,))}

    # Rule 1: First Steps (first quiz completion)
    if 'first_blood' not in existing:
        ach = query_db("SELECT id, title, icon, points FROM achievements WHERE slug = 'first_blood'", one=True)
        if ach:
            cursor.execute("INSERT OR IGNORE INTO user_achievements (user_id, achievement_id) VALUES (?, ?)", (user_id, ach['id']))
            cursor.execute("UPDATE users SET total_points = total_points + ? WHERE id = ?", (ach['points'], user_id))
            newly_unlocked.append(ach['title'])

    # Rule 2: Flawless Victory (100% on any quiz)
    if 'flawless_victory' not in existing and attempt_data.get('score_percentage', 0) >= 100.0:
        ach = query_db("SELECT id, title, icon, points FROM achievements WHERE slug = 'flawless_victory'", one=True)
        if ach:
            cursor.execute("INSERT OR IGNORE INTO user_achievements (user_id, achievement_id) VALUES (?, ?)", (user_id, ach['id']))
            cursor.execute("UPDATE users SET total_points = total_points + ? WHERE id = ?", (ach['points'], user_id))
            newly_unlocked.append(ach['title'])

    # Rule 3: Speed Demon (< 60s and score >= 80)
    if 'speed_demon' not in existing and attempt_data.get('time_taken_sec', 999) < 60 and attempt_data.get('score_percentage', 0) >= 80.0:
        ach = query_db("SELECT id, title, icon, points FROM achievements WHERE slug = 'speed_demon'", one=True)
        if ach:
            cursor.execute("INSERT OR IGNORE INTO user_achievements (user_id, achievement_id) VALUES (?, ?)", (user_id, ach['id']))
            cursor.execute("UPDATE users SET total_points = total_points + ? WHERE id = ?", (ach['points'], user_id))
            newly_unlocked.append(ach['title'])

    # Rule 4: Polyglot (attempted 3+ different topics)
    if 'polyglot' not in existing:
        distinct_topics = query_db("SELECT COUNT(DISTINCT topic_slug) AS cnt FROM quiz_attempts WHERE user_id = ?", (user_id,), one=True)
        if distinct_topics and distinct_topics['cnt'] >= 3:
            ach = query_db("SELECT id, title, icon, points FROM achievements WHERE slug = 'polyglot'", one=True)
            if ach:
                cursor.execute("INSERT OR IGNORE INTO user_achievements (user_id, achievement_id) VALUES (?, ?)", (user_id, ach['id']))
                cursor.execute("UPDATE users SET total_points = total_points + ? WHERE id = ?", (ach['points'], user_id))
                newly_unlocked.append(ach['title'])

    # Rule 5: Grandmaster (> 500 total points)
    if 'grandmaster' not in existing:
        user = query_db("SELECT total_points FROM users WHERE id = ?", (user_id,), one=True)
        if user and user['total_points'] >= 500:
            ach = query_db("SELECT id, title, icon, points FROM achievements WHERE slug = 'grandmaster'", one=True)
            if ach:
                cursor.execute("INSERT OR IGNORE INTO user_achievements (user_id, achievement_id) VALUES (?, ?)", (user_id, ach['id']))
                cursor.execute("UPDATE users SET total_points = total_points + ? WHERE id = ?", (ach['points'], user_id))
                newly_unlocked.append(ach['title'])

    db.commit()
    return newly_unlocked
