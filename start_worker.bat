@echo off
echo Starting worker process...
cd /d %~dp0
call venv\Scripts\activate
python -m app.worker
pause