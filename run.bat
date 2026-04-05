@echo off

REM Activate virtual environment (venv)
if not exist venv (
    echo [ERRO] Ambiente virtual 'venv' nao encontrado. Rode o setup_backend.bat primeiro!
    pause
    exit /b 1
)
call venv\Scripts\activate

REM Install requirements (garante que está sempre atualizado ao rodar)
echo Instalando/Atualizando dependencias...
call pip install -r requirements.txt

REM Start Docker Compose
echo Iniciando Docker Compose...
docker compose up -d

REM Wait for database to be ready
echo Waiting for database to be ready...
timeout /t 10 /nobreak > nul

REM Run the backend
echo Iniciando Uvicorn...
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload