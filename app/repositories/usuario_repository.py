from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from app.models.postgres.models import (
    DimUsuario,
)


def get_usuarios(db: Session) -> List[DimUsuario]:
    """Retorna todos os usuários cadastrados."""
    return db.query(DimUsuario).order_by(DimUsuario.id_usuario).all()


def get_usuario_by_id(db: Session, usuario_id: int) -> Optional[DimUsuario]:
    """Retorna um usuário pelo id_usuario. None se não existir."""
    return db.query(DimUsuario).filter(DimUsuario.id_usuario == usuario_id).first()


def get_usuario_by_nome(db: Session, nome_usuario: str) -> Optional[DimUsuario]:
    """Retorna um usuário pelo nome_usuario. None se não existir."""
    return db.query(DimUsuario).filter(DimUsuario.nome_usuario == nome_usuario).first()