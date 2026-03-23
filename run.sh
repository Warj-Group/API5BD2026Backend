#!/bin/bash

# Activate virtual environment
source venv/Scripts/activate

# Start Docker Compose
docker compose up -d

# Wait for database to be ready
echo "Waiting for database to be ready..."
sleep 10

# Run the backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload