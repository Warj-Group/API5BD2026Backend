from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from app.models.postgres.models import (
    DimPrograma,
)
def get_programas(db: Session) -> List[DimPrograma]:
    """Retorna todos os programas cadastrados."""
    return db.query(DimPrograma).order_by(DimPrograma.id_programa).all()


def get_programa_by_id(db: Session, programa_id: int) -> Optional[DimPrograma]:
    """Retorna um programa pelo id_programa. None se não existir."""
    return db.query(DimPrograma).filter(DimPrograma.id_programa == programa_id).first()


def get_programas_by_status(db: Session, status: str) -> List[DimPrograma]:
    """Filtra programas por status (ex: 'ativo', 'encerrado')."""
    return db.query(DimPrograma).filter(DimPrograma.status == status).all()