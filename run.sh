#!/bin/bash

# Activate virtual environment (venv)
if [ ! -d "venv" ]; then
    echo "❌ ERRO: Ambiente virtual 'venv' não encontrado. Rode o setup_backend.sh primeiro!"
    exit 1
fi
source venv/bin/activate

# Install requirements (garante que está sempre atualizado ao rodar)
echo "📦 Instalando/Atualizando dependências..."
pip install -r requirements.txt

# Start Docker Compose
echo "🐳 Iniciando Docker Compose..."
docker compose up -d

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
sleep 10

# Run the backend
echo "🚀 Iniciando Uvicorn..."
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload