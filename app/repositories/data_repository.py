from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from app.models.postgres.models import (
    DimData,
)


def get_datas(db: Session) -> List[DimData]:
    """Retorna todas as entradas da dimensão de datas."""
    return db.query(DimData).order_by(DimData.data.desc()).all()


def get_data_by_id(db: Session, data_id: int) -> Optional[DimData]:
    """Retorna uma entrada de data pelo id_data. None se não existir."""
    return db.query(DimData).filter(DimData.id_data == data_id).first()


def get_datas_by_ano(db: Session, ano: int) -> List[DimData]:
    """Filtra entradas da dimensão de datas por ano."""
    return db.query(DimData).filter(DimData.ano == ano).order_by(DimData.data.desc()).all()


def get_datas_by_mes_ano(db: Session, mes: int, ano: int) -> List[DimData]:
    """Filtra entradas da dimensão de datas por mês e ano."""
    return db.query(DimData).filter(
        DimData.mes == mes,
        DimData.ano == ano,
    ).order_by(DimData.data.desc()).all()