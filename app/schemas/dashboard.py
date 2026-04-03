from decimal import Decimal
from pydantic import BaseModel, ConfigDict


class DashboardProjetoResponse(BaseModel):
    id_projeto: int
    codigo_projeto: str | None
    nome_projeto: str | None
    responsavel: str | None
    status: str | None
    custo_hora: Decimal
    total_horas: Decimal
    custo_materiais: Decimal
    custo_horas: Decimal
    custo_total: Decimal

    model_config = ConfigDict(from_attributes=True)