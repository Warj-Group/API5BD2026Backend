from datetime import date
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.postgres.models import (
    DimData,
)


def get_datas(db: Session) -> List[DimData]:
    """Retorna todas as entradas da dimensão de datas."""
    return db.query(DimData).order_by(DimData.data.desc()).all()


def get_data_by_id(db: Session, data_id: int) -> Optional[DimData]:
    """Retorna uma entrada de data pelo id_data. None se não existir."""
    return db.query(DimData).filter(DimData.id_data == data_id).first()


def get_data_by_data(db: Session, data: date) -> Optional[DimData]:
    """Retorna uma entrada de data pela data. None se não existir."""
    return db.query(DimData).filter(DimData.data == data).first()


def get_datas_by_mes(db: Session, mes: int) -> List[DimData]:
    """Filtra entradas da dimensão de datas por mês."""
    return (
        db.query(DimData).filter(DimData.mes == mes).order_by(DimData.data.desc()).all()
    )


def get_datas_by_nome_mes(db: Session, nome_mes: str) -> List[DimData]:
    """Filtra entradas da dimensão de datas por nome do mês."""
    return (
        db.query(DimData)
        .filter(DimData.nome_mes == nome_mes)
        .order_by(DimData.data.desc())
        .all()
    )
