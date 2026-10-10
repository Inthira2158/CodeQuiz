import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'codequiz-secret-key-2026-supersecure')
    DATABASE = os.path.join(BASE_DIR, 'codequiz.db')
    DEBUG = True
    QUESTIONS_PER_PAGE = 10
    DEFAULT_QUIZ_TIME_LIMIT_PER_Q = 30  # seconds per question
