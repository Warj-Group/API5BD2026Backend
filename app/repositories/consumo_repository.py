from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.postgres.models import (
    FactConsumoMateriais,
)


def get_consumo_materiais(db: Session) -> List[FactConsumoMateriais]:
    """Retorna todos os registros de consumo de materiais."""
    return (
        db.query(FactConsumoMateriais)
        .order_by(FactConsumoMateriais.id_fato_material)
        .all()
    )


def get_consumo_by_id(db: Session, fato_id: int) -> Optional[FactConsumoMateriais]:
    """Retorna um registro de consumo pelo id_fato_material. None se não existir."""
    return (
        db.query(FactConsumoMateriais)
        .filter(FactConsumoMateriais.id_fato_material == fato_id)
        .first()
    )


def get_consumo_by_projeto(db: Session, projeto_id: int) -> List[FactConsumoMateriais]:
    """Filtra consumo de materiais por projeto."""
    return (
        db.query(FactConsumoMateriais)
        .filter(FactConsumoMateriais.projeto_id == projeto_id)
        .all()
    )


def get_consumo_by_material(
    db: Session, material_id: int
) -> List[FactConsumoMateriais]:
    """Filtra consumo de materiais por material."""
    return (
        db.query(FactConsumoMateriais)
        .filter(FactConsumoMateriais.material_id == material_id)
        .all()
    )


def get_consumo_by_fornecedor(
    db: Session, fornecedor_id: int
) -> List[FactConsumoMateriais]:
    """Filtra consumo de materiais por fornecedor."""
    return (
        db.query(FactConsumoMateriais)
        .filter(FactConsumoMateriais.fornecedor_id == fornecedor_id)
        .all()
    )


def get_custo_total_by_projeto(db: Session, projeto_id: int) -> float:
    """
    Retorna a soma do custo_total de todos os consumos de um projeto.
    Retorna 0.0 se não houver registros.
    """
    resultado = (
        db.query(func.sum(FactConsumoMateriais.custo_total))
        .filter(FactConsumoMateriais.projeto_id == projeto_id)
        .scalar()
    )
    return resultado or 0.0


def get_quantidade_total_by_material(db: Session, material_id: int) -> float:
    """
    Retorna a soma da quantidade_empenhada de um material em todos os projetos.
    Retorna 0.0 se não houver registros.
    """
    resultado = (
        db.query(func.sum(FactConsumoMateriais.quantidade_empenhada))
        .filter(FactConsumoMateriais.material_id == material_id)
        .scalar()
    )
    return resultado or 0.0


def get_custo_total_by_fornecedor(db: Session, fornecedor_id: int) -> float:
    """
    Retorna a soma do custo_total de um fornecedor em todos os consumos.
    Retorna 0.0 se não houver registros.
    """
    resultado = (
        db.query(func.sum(FactConsumoMateriais.custo_total))
        .filter(FactConsumoMateriais.fornecedor_id == fornecedor_id)
        .scalar()
    )
    return resultado or 0.0
