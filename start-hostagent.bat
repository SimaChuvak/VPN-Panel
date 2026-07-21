@echo off
cd /d "%~dp0hostagent"
echo Starting HostAgent server...
py -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
pause
