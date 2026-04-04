from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.postgres.models import (
    FactCompras,
)


def get_compras(db: Session) -> List[FactCompras]:
    """Retorna todos os registros de compras."""
    return db.query(FactCompras).order_by(FactCompras.id_fato_compra).all()


def get_compra_by_id(db: Session, fato_id: int) -> Optional[FactCompras]:
    """Retorna um registro de compra pelo id_fato_compra. None se não existir."""
    return db.query(FactCompras).filter(FactCompras.id_fato_compra == fato_id).first()


def get_compras_by_pedido(db: Session, pedido_id: int) -> List[FactCompras]:
    """Filtra compras por pedido."""
    return db.query(FactCompras).filter(FactCompras.pedido_id == pedido_id).all()


def get_compras_by_projeto(db: Session, projeto_id: int) -> List[FactCompras]:
    """Filtra compras por projeto."""
    return db.query(FactCompras).filter(FactCompras.projeto_id == projeto_id).all()


def get_compras_by_fornecedor(db: Session, fornecedor_id: int) -> List[FactCompras]:
    """Filtra compras por fornecedor."""
    return (
        db.query(FactCompras).filter(FactCompras.fornecedor_id == fornecedor_id).all()
    )


def get_valor_total_by_projeto(db: Session, projeto_id: int) -> float:
    """
    Retorna a soma do valor_total de compras de um projeto.
    Retorna 0.0 se não houver registros.
    """
    resultado = (
        db.query(func.sum(FactCompras.valor_total))
        .filter(FactCompras.projeto_id == projeto_id)
        .scalar()
    )
    return resultado or 0.0


def get_valor_total_by_fornecedor(db: Session, fornecedor_id: int) -> float:
    """
    Retorna a soma do valor_total de compras de um fornecedor.
    Retorna 0.0 se não houver registros.
    """
    resultado = (
        db.query(func.sum(FactCompras.valor_total))
        .filter(FactCompras.fornecedor_id == fornecedor_id)
        .scalar()
    )
    return resultado or 0.0
