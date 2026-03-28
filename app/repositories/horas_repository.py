from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from app.models.postgres.models import (
    FactHorasTrabalhadas,
)


def get_horas_trabalhadas(db: Session) -> List[FactHorasTrabalhadas]:
    """Retorna todos os registros de horas trabalhadas."""
    return db.query(FactHorasTrabalhadas).order_by(FactHorasTrabalhadas.id_fato_horas).all()


def get_horas_by_id(db: Session, fato_id: int) -> Optional[FactHorasTrabalhadas]:
    """Retorna um registro de horas pelo id_fato_horas. None se não existir."""
    return db.query(FactHorasTrabalhadas).filter(
        FactHorasTrabalhadas.id_fato_horas == fato_id
    ).first()


def get_horas_by_programa(db: Session, programa_id: int) -> List[FactHorasTrabalhadas]:
    """Filtra horas trabalhadas por programa."""
    return db.query(FactHorasTrabalhadas).filter(
        FactHorasTrabalhadas.programa_id == programa_id
    ).all()


def get_horas_by_projeto(db: Session, projeto_id: int) -> List[FactHorasTrabalhadas]:
    """Filtra horas trabalhadas por projeto."""
    return db.query(FactHorasTrabalhadas).filter(
        FactHorasTrabalhadas.projeto_id == projeto_id
    ).all()


def get_horas_by_usuario(db: Session, usuario_id: int) -> List[FactHorasTrabalhadas]:
    """Filtra horas trabalhadas por usuário."""
    return db.query(FactHorasTrabalhadas).filter(
        FactHorasTrabalhadas.usuario_id == usuario_id
    ).all()


def get_horas_by_tarefa(db: Session, tarefa_id: int) -> List[FactHorasTrabalhadas]:
    """Filtra horas trabalhadas por tarefa."""
    return db.query(FactHorasTrabalhadas).filter(
        FactHorasTrabalhadas.tarefa_id == tarefa_id
    ).all()


def get_total_horas_by_projeto(db: Session, projeto_id: int) -> float:
    """
    Retorna a soma de horas_trabalhadas de um projeto.
    Retorna 0.0 se não houver registros.
    """
    resultado = db.query(func.sum(FactHorasTrabalhadas.horas_trabalhadas)).filter(
        FactHorasTrabalhadas.projeto_id == projeto_id
    ).scalar()
    return resultado or 0.0


def get_total_horas_by_usuario(db: Session, usuario_id: int) -> float:
    """
    Retorna a soma de horas_trabalhadas de um usuário.
    Retorna 0.0 se não houver registros.
    """
    resultado = db.query(func.sum(FactHorasTrabalhadas.horas_trabalhadas)).filter(
        FactHorasTrabalhadas.usuario_id == usuario_id
    ).scalar()
    return resultado or 0.0


def get_total_horas_by_programa(db: Session, programa_id: int) -> float:
    """
    Retorna a soma de horas_trabalhadas de todos os projetos de um programa.
    Retorna 0.0 se não houver registros.
    """
    resultado = db.query(func.sum(FactHorasTrabalhadas.horas_trabalhadas)).filter(
        FactHorasTrabalhadas.programa_id == programa_id
    ).scalar()
    return resultado or 0.0