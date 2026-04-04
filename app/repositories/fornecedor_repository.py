from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.postgres.models import (
    DimFornecedor,
)


def get_fornecedores(db: Session) -> List[DimFornecedor]:
    """Retorna todos os fornecedores cadastrados."""
    return db.query(DimFornecedor).order_by(DimFornecedor.id_fornecedor).all()


def get_fornecedor_by_id(db: Session, fornecedor_id: int) -> Optional[DimFornecedor]:
    """Retorna um fornecedor pelo id_fornecedor. None se não existir."""
    return (
        db.query(DimFornecedor)
        .filter(DimFornecedor.id_fornecedor == fornecedor_id)
        .first()
    )


def get_fornecedor_by_codigo(
    db: Session, codigo_fornecedor: str
) -> Optional[DimFornecedor]:
    """Retorna um fornecedor pelo codigo_fornecedor. None se não existir."""
    return (
        db.query(DimFornecedor)
        .filter(DimFornecedor.codigo_fornecedor == codigo_fornecedor)
        .first()
    )


def get_fornecedores_by_estado(db: Session, estado: str) -> List[DimFornecedor]:
    """Filtra fornecedores por estado (UF)."""
    return (
        db.query(DimFornecedor)
        .filter(DimFornecedor.estado == estado)
        .order_by(DimFornecedor.id_fornecedor)
        .all()
    )
