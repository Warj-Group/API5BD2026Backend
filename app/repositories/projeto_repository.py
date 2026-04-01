from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from app.models.postgres.models import (
    DimProjeto,
)


def get_projetos(db: Session) -> List[DimProjeto]:
    """Retorna todos os projetos cadastrados."""
    return db.query(DimProjeto).order_by(DimProjeto.id_projeto).all()


def get_projeto_by_id(db: Session, projeto_id: int) -> Optional[DimProjeto]:
    """Retorna um projeto pelo id_projeto. None se não existir."""
    return db.query(DimProjeto).filter(DimProjeto.id_projeto == projeto_id).first()


def get_projeto_by_codigo(db: Session, codigo_projeto: str) -> Optional[DimProjeto]:
    """Retorna um projeto pelo codigo_projeto. None se não existir."""
    return db.query(DimProjeto).filter(DimProjeto.codigo_projeto == codigo_projeto).first()


def get_projetos_by_programa(db: Session, programa_id: int) -> List[DimProjeto]:
    """Retorna todos os projetos vinculados a um programa."""
    return db.query(DimProjeto).filter(DimProjeto.programa_id == programa_id).order_by(DimProjeto.id_projeto).all()
