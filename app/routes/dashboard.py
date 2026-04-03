from decimal import Decimal

from fastapi import APIRouter, Depends
from sqlalchemy import Numeric, cast, func
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.postgres.models import (
    DimProjeto,
    FactConsumoMateriais,
    FactHorasTrabalhadas,
)
from app.schemas.dashboard import (
    DashboardProjetoResponse,
    DashboardResumoResponse,
)

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


def _build_dashboard_cost_query(db: Session):
    materiais_subquery = (
        db.query(
            FactConsumoMateriais.projeto_id.label("projeto_id"),
            func.coalesce(
                func.sum(FactConsumoMateriais.custo_total),
                0
            ).label("custo_materiais"),
        )
        .group_by(FactConsumoMateriais.projeto_id)
        .subquery()
    )

    horas_subquery = (
        db.query(
            FactHorasTrabalhadas.projeto_id.label("projeto_id"),
            func.coalesce(
                func.sum(FactHorasTrabalhadas.horas_trabalhadas),
                0
            ).label("total_horas"),
        )
        .group_by(FactHorasTrabalhadas.projeto_id)
        .subquery()
    )

    custo_hora_expr = func.coalesce(DimProjeto.custo_hora, 0)
    total_horas_expr = func.coalesce(horas_subquery.c.total_horas, 0)
    custo_materiais_expr = func.coalesce(materiais_subquery.c.custo_materiais, 0)

    custo_horas_expr = cast(
        total_horas_expr * custo_hora_expr,
        Numeric(12, 2)
    )

    custo_total_expr = cast(
        custo_materiais_expr + custo_horas_expr,
        Numeric(12, 2)
    )

    base_query = (
        db.query(
            DimProjeto.id_projeto.label("id_projeto"),
            DimProjeto.codigo_projeto.label("codigo_projeto"),
            DimProjeto.nome_projeto.label("nome_projeto"),
            DimProjeto.responsavel.label("responsavel"),
            DimProjeto.status.label("status"),
            cast(custo_hora_expr, Numeric(10, 2)).label("custo_hora"),
            cast(total_horas_expr, Numeric(10, 2)).label("total_horas"),
            cast(custo_materiais_expr, Numeric(12, 2)).label("custo_materiais"),
            custo_horas_expr.label("custo_horas"),
            custo_total_expr.label("custo_total"),
        )
        .outerjoin(
            materiais_subquery,
            DimProjeto.id_projeto == materiais_subquery.c.projeto_id
        )
        .outerjoin(
            horas_subquery,
            DimProjeto.id_projeto == horas_subquery.c.projeto_id
        )
    )

    return base_query


@router.get("/projetos", response_model=list[DashboardProjetoResponse])
async def get_dashboard_projetos(db: Session = Depends(get_db)):
    resultados = (
        _build_dashboard_cost_query(db)
        .order_by(DimProjeto.nome_projeto.asc())
        .all()
    )

    return [
        DashboardProjetoResponse(
            id_projeto=row.id_projeto,
            codigo_projeto=row.codigo_projeto,
            nome_projeto=row.nome_projeto,
            responsavel=row.responsavel,
            status=row.status,
            custo_hora=row.custo_hora or Decimal("0.00"),
            total_horas=row.total_horas or Decimal("0.00"),
            custo_materiais=row.custo_materiais or Decimal("0.00"),
            custo_horas=row.custo_horas or Decimal("0.00"),
            custo_total=row.custo_total or Decimal("0.00"),
        )
        for row in resultados
    ]


@router.get("/resumo", response_model=DashboardResumoResponse)
async def get_dashboard_resumo(db: Session = Depends(get_db)):
    base_subquery = _build_dashboard_cost_query(db).subquery()

    resultado = (
        db.query(
            func.count(base_subquery.c.id_projeto).label("total_projetos"),
            cast(
                func.coalesce(func.sum(base_subquery.c.custo_materiais), 0),
                Numeric(12, 2)
            ).label("custo_materiais_geral"),
            cast(
                func.coalesce(func.sum(base_subquery.c.total_horas), 0),
                Numeric(12, 2)
            ).label("total_horas_geral"),
            cast(
                func.coalesce(func.sum(base_subquery.c.custo_horas), 0),
                Numeric(12, 2)
            ).label("custo_horas_geral"),
            cast(
                func.coalesce(func.sum(base_subquery.c.custo_total), 0),
                Numeric(12, 2)
            ).label("custo_total_geral"),
            cast(
                func.coalesce(func.avg(base_subquery.c.custo_total), 0),
                Numeric(12, 2)
            ).label("custo_medio_por_projeto"),
        )
        .one()
    )

    return DashboardResumoResponse(
        total_projetos=resultado.total_projetos or 0,
        custo_total_geral=resultado.custo_total_geral or Decimal("0.00"),
        custo_medio_por_projeto=resultado.custo_medio_por_projeto or Decimal("0.00"),
        total_horas_geral=resultado.total_horas_geral or Decimal("0.00"),
        custo_materiais_geral=resultado.custo_materiais_geral or Decimal("0.00"),
        custo_horas_geral=resultado.custo_horas_geral or Decimal("0.00"),
    )