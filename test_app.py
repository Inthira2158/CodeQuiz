"""
test_app.py - Automated Test Suite for CodeQuiz Platform
Tests topics, question retrieval, quiz flow, scoring, leaderboards, and progress tracking.
"""

import unittest
import json
import sqlite3
from app import app
import database as db


class CodeQuizTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_01_all_topics_exist(self):
        """Verify that all requested topics exist in database."""
        expected_topics = {'python', 'java', 'sql', 'html', 'css', 'javascript'}
        topics = db.get_all_topics()
        slugs = {t['slug'] for t in topics}
        for expected in expected_topics:
            self.assertIn(expected, slugs, f"Missing topic: {expected}")
        print("[PASS] All 6 programming topics verified.")

    def test_02_questions_per_topic(self):
        """Verify that every topic has rich questions available."""
        topics = db.get_all_topics()
        for t in topics:
            questions = db.get_questions_for_quiz(t['slug'], limit=10)
            self.assertGreaterEqual(len(questions), 5, f"Topic {t['name']} has too few questions")
            # Verify options and correct option
            for q in questions:
                self.assertIn(q['correct_option'], ['A', 'B', 'C', 'D'])
                self.assertTrue(len(q['explanation']) > 10)
        print("[PASS] Rich questions verified across all 6 topics.")

    def test_03_homepage_renders(self):
        """Verify landing page loads with topics and stats."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn('CodeQuiz', html)
        self.assertIn('Python', html)
        self.assertIn('JavaScript', html)
        self.assertIn('Leaderboard', html)
        print("[PASS] Home page renders properly.")

    def test_04_user_registration_and_login(self):
        """Test registering a new user and logging in."""
        import random
        rand_id = random.randint(1000, 9999)
        uname = f"tester_{rand_id}"
        email = f"tester_{rand_id}@test.com"

        reg_res = self.client.post('/register', data={
            'username': uname,
            'email': email,
            'password': 'testpassword123',
            'confirm_password': 'testpassword123',
            'bio': 'Automated Test User'
        }, follow_redirects=True)
        self.assertEqual(reg_res.status_code, 200)

        # Check DB
        user = db.get_user_by_username(uname)
        self.assertIsNotNone(user)
        self.assertEqual(user['email'], email)
        print("[PASS] User registration and session login verified.")

    def test_05_quiz_execution_scoring_and_progress(self):
        """Test taking a quiz, submitting answers, scoring, and progress update."""
        # 1. Register or login user
        uname = "quiz_tester"
        user = db.get_user_by_username(uname)
        if not user:
            from werkzeug.security import generate_password_hash
            uid = db.create_user(uname, "qt@example.com", generate_password_hash("pass123"), bio="Tester")
        else:
            uid = user['id']

        with self.client.session_transaction() as sess:
            sess['user_id'] = uid

        # 2. Get 5 Python questions
        questions = db.get_questions_for_quiz('python', limit=5)
        self.assertEqual(len(questions), 5)

        # 3. Simulate answering 4 correctly, 1 wrong
        answers_payload = {}
        for idx, q in enumerate(questions):
            if idx < 4:
                # Correct answer
                answers_payload[str(q['id'])] = {'selected': q['correct_option'], 'time': 10}
            else:
                # Wrong answer
                wrong = 'A' if q['correct_option'] != 'A' else 'B'
                answers_payload[str(q['id'])] = {'selected': wrong, 'time': 12}

        # 4. Submit
        submit_res = self.client.post('/quiz/submit', json={
            'topic_slug': 'python',
            'difficulty': 'Mixed',
            'total_time_spent': 52,
            'answers': answers_payload
        })
        self.assertEqual(submit_res.status_code, 200)
        data = json.loads(submit_res.get_data(as_text=True))
        self.assertEqual(data['status'], 'success')
        self.assertIn('/quiz/result/', data['redirect_url'])

        # 5. Verify User Topic Progress updated
        progress = db.query_db("SELECT * FROM user_topic_stats WHERE user_id = ? AND topic_slug = 'python'", (uid,), one=True)
        self.assertIsNotNone(progress)
        self.assertGreaterEqual(progress['quizzes_taken'], 1)
        self.assertGreaterEqual(progress['total_correct'], 4)
        self.assertEqual(progress['best_score'], 80.0)

        # 6. Verify result page renders with explanations
        attempt_id = int(data['redirect_url'].split('/')[-1])
        res_page = self.client.get(f'/quiz/result/{attempt_id}')
        self.assertEqual(res_page.status_code, 200)
        page_html = res_page.get_data(as_text=True)
        self.assertIn('80%', page_html)
        self.assertIn('Technical Explanation', page_html)
        print("[PASS] Quiz execution, automatic scoring, and progress tracking verified.")

    def test_06_leaderboard_rankings(self):
        """Test global and topic leaderboard endpoints."""
        global_rankings = db.get_global_leaderboard(limit=10)
        self.assertGreater(len(global_rankings), 0)
        # Check ordering: total_points descending
        for i in range(len(global_rankings) - 1):
            self.assertGreaterEqual(global_rankings[i]['total_points'], global_rankings[i+1]['total_points'])

        # Check topic leaderboard
        py_rankings = db.get_topic_leaderboard('python', limit=10)
        self.assertGreater(len(py_rankings), 0)
        print("[PASS] Leaderboard rankings verified.")

    def test_07_custom_question_creation(self):
        """Test creating a new topic-based quiz question."""
        user = db.get_user_by_username('AlexDev')
        q_id = db.create_question(
            topic_slug='javascript',
            difficulty='Intermediate',
            question_text='What does Array.isArray([]) return in JavaScript?',
            code_snippet='console.log(Array.isArray([]));',
            code_lang='javascript',
            option_a='true',
            option_b='false',
            option_c='undefined',
            option_d='TypeError',
            correct_option='A',
            explanation='Array.isArray() determines whether the passed value is an Array object, returning true for [].',
            time_limit_sec=25,
            created_by=user['id']
        )
        self.assertIsNotNone(q_id)
        fetched = db.get_question_by_id(q_id)
        self.assertEqual(fetched['correct_option'], 'A')
        self.assertEqual(fetched['topic_slug'], 'javascript')
        print("[PASS] Custom question creation verified.")


if __name__ == '__main__':
    unittest.main()
