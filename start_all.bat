@echo off
echo Starting Snaxa Vending application...
cd /d %~dp0
start cmd /k "start_worker.bat"
timeout /t 5
start cmd /k "run.bat"
echo Started all components.