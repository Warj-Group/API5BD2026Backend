from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.postgres.models import (
    DimTarefa,
)


def get_tarefas(db: Session) -> List[DimTarefa]:
    """Retorna todas as tarefas cadastradas."""
    return db.query(DimTarefa).order_by(DimTarefa.id_tarefa).all()


def get_tarefa_by_id(db: Session, tarefa_id: int) -> Optional[DimTarefa]:
    """Retorna uma tarefa pelo id_tarefa. None se não existir."""
    return db.query(DimTarefa).filter(DimTarefa.id_tarefa == tarefa_id).first()


def get_tarefa_by_codigo(db: Session, codigo_tarefa: str) -> Optional[DimTarefa]:
    """Retorna uma tarefa pelo codigo_tarefa. None se não existir."""
    return db.query(DimTarefa).filter(DimTarefa.codigo_tarefa == codigo_tarefa).first()


def get_tarefas_by_status(db: Session, status: str) -> List[DimTarefa]:
    """Filtra tarefas por status."""
    return (
        db.query(DimTarefa)
        .filter(DimTarefa.status == status)
        .order_by(DimTarefa.id_tarefa)
        .all()
    )
