@echo off

REM Activate virtual environment
call venv\Scripts\activate

REM Install requirements if needed
REM pip install -r requirements.txt

REM Start Docker Compose
docker compose up -d

REM Wait for database to be ready
echo Waiting for database to be ready...
timeout /t 10 /nobreak > nul

REM Run the backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload