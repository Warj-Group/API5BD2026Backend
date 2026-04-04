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


class DashboardResumoResponse(BaseModel):
    total_projetos: int
    custo_total_geral: Decimal
    custo_medio_por_projeto: Decimal
    total_horas_geral: Decimal
    custo_materiais_geral: Decimal
    custo_horas_geral: Decimal

    model_config = ConfigDict(from_attributes=True)
