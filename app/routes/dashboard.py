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


def _safe_decimal(value):
    if value is None or (
        isinstance(value, Decimal)
        and (value.is_nan() or value.is_infinite())
    ):
        return Decimal("0.00")
    return value

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("", response_model=DashboardResumoResponse)
async def get_dashboard_root(db: Session = Depends(get_db)):
    return await get_dashboard_resumo(db)


def _build_dashboard_cost_query(db: Session):
    materiais_subquery = (
        db.query(
            FactConsumoMateriais.projeto_id.label("projeto_id"),
            func.coalesce(func.sum(FactConsumoMateriais.custo_total), 0).label(
                "custo_materiais"
            ),
        )
        .group_by(FactConsumoMateriais.projeto_id)
        .subquery()
    )

    horas_subquery = (
        db.query(
            FactHorasTrabalhadas.projeto_id.label("projeto_id"),
            func.coalesce(func.sum(FactHorasTrabalhadas.horas_trabalhadas), 0).label(
                "total_horas"
            ),
        )
        .group_by(FactHorasTrabalhadas.projeto_id)
        .subquery()
    )

    custo_hora_expr = func.coalesce(DimProjeto.custo_hora, 0)
    total_horas_expr = func.coalesce(horas_subquery.c.total_horas, 0)
    custo_materiais_expr = func.coalesce(materiais_subquery.c.custo_materiais, 0)

    custo_horas_expr = cast(total_horas_expr * custo_hora_expr, Numeric(12, 2))

    custo_total_expr = cast(custo_materiais_expr + custo_horas_expr, Numeric(12, 2))

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
            materiais_subquery, DimProjeto.id_projeto == materiais_subquery.c.projeto_id
        )
        .outerjoin(horas_subquery, DimProjeto.id_projeto == horas_subquery.c.projeto_id)
    )

    return base_query


@router.get("/projetos", response_model=list[DashboardProjetoResponse])
async def get_dashboard_projetos(db: Session = Depends(get_db)):
    resultados = (
        _build_dashboard_cost_query(db).order_by(DimProjeto.nome_projeto.asc()).all()
    )

    return [
        DashboardProjetoResponse(
            id_projeto=row.id_projeto,
            codigo_projeto=row.codigo_projeto,
            nome_projeto=row.nome_projeto,
            responsavel=row.responsavel,
            status=row.status,
            custo_hora=_safe_decimal(row.custo_hora),
            total_horas=_safe_decimal(row.total_horas),
            custo_materiais=_safe_decimal(row.custo_materiais),
            custo_horas=_safe_decimal(row.custo_horas),
            custo_total=_safe_decimal(row.custo_total),
        )
        for row in resultados
    ]


@router.get("/resumo", response_model=DashboardResumoResponse)
async def get_dashboard_resumo(db: Session = Depends(get_db)):
    base_subquery = _build_dashboard_cost_query(db).subquery()

    resultado = db.query(
        func.count(base_subquery.c.id_projeto).label("total_projetos"),
        cast(
            func.coalesce(func.sum(base_subquery.c.custo_materiais), 0), Numeric(12, 2)
        ).label("custo_materiais_geral"),
        cast(
            func.coalesce(func.sum(base_subquery.c.total_horas), 0), Numeric(12, 2)
        ).label("total_horas_geral"),
        cast(
            func.coalesce(func.sum(base_subquery.c.custo_horas), 0), Numeric(12, 2)
        ).label("custo_horas_geral"),
        cast(
            func.coalesce(func.sum(base_subquery.c.custo_total), 0), Numeric(12, 2)
        ).label("custo_total_geral"),
        cast(
            func.coalesce(func.avg(base_subquery.c.custo_total), 0), Numeric(12, 2)
        ).label("custo_medio_por_projeto"),
    ).one()

    return DashboardResumoResponse(
        total_projetos=resultado.total_projetos or 0,
        custo_total_geral=_safe_decimal(resultado.custo_total_geral),
        custo_medio_por_projeto=_safe_decimal(resultado.custo_medio_por_projeto),
        total_horas_geral=_safe_decimal(resultado.total_horas_geral),
        custo_materiais_geral=_safe_decimal(resultado.custo_materiais_geral),
        custo_horas_geral=_safe_decimal(resultado.custo_horas_geral),
    )
