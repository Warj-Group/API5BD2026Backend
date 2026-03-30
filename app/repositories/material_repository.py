from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from app.models.postgres.models import (
    DimMaterial,
)

def get_materiais(db: Session) -> List[DimMaterial]:
    """Retorna todos os materiais cadastrados."""
    return db.query(DimMaterial).order_by(DimMaterial.id_material).all()


def get_material_by_id(db: Session, material_id: int) -> Optional[DimMaterial]:
    """Retorna um material pelo id_material. None se não existir."""
    return db.query(DimMaterial).filter(DimMaterial.id_material == material_id).first()


def get_material_by_codigo(db: Session, codigo_material: str) -> Optional[DimMaterial]:
    """Retorna um material pelo codigo_material. None se não existir."""
    return db.query(DimMaterial).filter(DimMaterial.codigo_material == codigo_material).first()


def get_materiais_by_categoria(db: Session, categoria: str) -> List[DimMaterial]:
    """Filtra materiais por categoria."""
    return db.query(DimMaterial).filter(DimMaterial.categoria == categoria).order_by(DimMaterial.id_material).all()