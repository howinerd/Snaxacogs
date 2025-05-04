@echo off
echo Starting Flask application...
cd /d %~dp0
call venv\Scripts\activate
python run.py
pause