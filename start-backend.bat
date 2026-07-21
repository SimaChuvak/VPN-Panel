@echo off
cd /d "%~dp0backend"
echo Applying database migrations...
py -m alembic upgrade head
echo.
echo Starting Backend server...
py -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
pause
