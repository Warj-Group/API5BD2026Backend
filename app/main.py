from fastapi import FastAPI
from sqlalchemy import text

from app.db.database import SessionLocal
from app.routes.data import router as data_router

app = FastAPI(
    title="DW Projeto API",
    version="2.0.0",
    description="API compatível com o schema gerado pelo ETL v2 em modelo estrela.",
)

app.include_router(data_router)


@app.get("/")
def root():
    return {
        "message": "API Python para consulta do Data Warehouse Projeto",
        "version": "2.0.0",
        "status": "online",
        "compatibility": "etl_backend_star_v2",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    finally:
        db.close()
