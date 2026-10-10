@echo off
title CodeQuiz - Programming Quiz Platform
echo ========================================================
echo   Starting CodeQuiz Platform...
echo ========================================================
echo.

cd /d "%~dp0"

echo [1/3] Checking dependencies...
python -m pip install -r requirements.txt --quiet

echo [2/3] Checking database...
if not exist "codequiz.db" (
    echo Seeding CodeQuiz database with question bank and topics...
    python seed_data.py
)

echo [3/3] Opening browser and starting server on http://127.0.0.1:5000 ...
start http://127.0.0.1:5000

python app.py
pause
