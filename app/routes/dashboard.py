from __future__ import annotations

from datetime import date
from decimal import Decimal

from fastapi import APIRouter, Depends, Query
from sqlalchemy import Numeric, and_, case, cast, func, literal
from sqlalchemy.orm import Session, aliased

from app.db.database import get_db
from app.models.postgres.models import (
    DimData,
    DimProjeto,
    FactConsumoMateriais,
    FactHorasTrabalhadas,
)
from app.schemas.dashboard import (
    DashboardProjetoResponse,
    DashboardResumoResponse,
)

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


def _safe_decimal(value) -> Decimal:
    if value is None:
        return Decimal("0.00")

    if isinstance(value, Decimal):
        if value.is_nan() or value.is_infinite():
            return Decimal("0.00")
        return value

    try:
        return Decimal(str(value))
    except Exception:
        return Decimal("0.00")


def _build_period_filters(data_alias, data_inicio: date | None, data_fim: date | None):
    filters = []

    if data_inicio is not None:
        filters.append(data_alias.data >= data_inicio)

    if data_fim is not None:
        filters.append(data_alias.data <= data_fim)

    return filters


def _build_dashboard_cost_query(
    db: Session,
    data_inicio: date | None = None,
    data_fim: date | None = None,
):
    """
    Monta a query base do dashboard com:
    - agregação por projeto
    - fallback para custo de materiais
    - filtro opcional por período via dim_data
    """

    data_horas = aliased(DimData)
    data_materiais = aliased(DimData)

    # ----------------------------
    # Subquery de HORAS
    # ----------------------------
    horas_filters = _build_period_filters(data_horas, data_inicio, data_fim)

    # Observação:
    # Se o banco estiver contendo NaN em numeric, ideal é limpar no ETL/banco.
    # Aqui fazemos a agregação assumindo que os valores válidos são somáveis.
    horas_subquery = (
        db.query(
            FactHorasTrabalhadas.projeto_id.label("projeto_id"),
            cast(
                func.coalesce(
                    func.sum(func.coalesce(FactHorasTrabalhadas.horas_trabalhadas, 0)),
                    0,
                ),
                Numeric(12, 2),
            ).label("total_horas"),
        )
        .outerjoin(
            data_horas,
            FactHorasTrabalhadas.data_id == data_horas.id_data,
        )
        .filter(FactHorasTrabalhadas.projeto_id.isnot(None))
    )

    if horas_filters:
        horas_subquery = horas_subquery.filter(and_(*horas_filters))

    horas_subquery = horas_subquery.group_by(FactHorasTrabalhadas.projeto_id).subquery()

    # ----------------------------
    # Subquery de MATERIAIS
    # ----------------------------
    materiais_filters = _build_period_filters(data_materiais, data_inicio, data_fim)

    # Fallback:
    # - usa custo_total quando preenchido e diferente de zero
    # - senão calcula quantidade_empenhada * custo_unitario
    custo_material_linha = case(
        (
            and_(
                FactConsumoMateriais.custo_total.isnot(None),
                FactConsumoMateriais.custo_total != 0,
            ),
            FactConsumoMateriais.custo_total,
        ),
        else_=(
            func.coalesce(FactConsumoMateriais.quantidade_empenhada, 0)
            * func.coalesce(FactConsumoMateriais.custo_unitario, 0)
        ),
    )

    materiais_subquery = (
        db.query(
            FactConsumoMateriais.projeto_id.label("projeto_id"),
            cast(
                func.coalesce(func.sum(custo_material_linha), 0),
                Numeric(12, 2),
            ).label("custo_materiais"),
        )
        .outerjoin(
            data_materiais,
            FactConsumoMateriais.data_id == data_materiais.id_data,
        )
        .filter(FactConsumoMateriais.projeto_id.isnot(None))
    )

    if materiais_filters:
        materiais_subquery = materiais_subquery.filter(and_(*materiais_filters))

    materiais_subquery = materiais_subquery.group_by(
        FactConsumoMateriais.projeto_id
    ).subquery()

    # ----------------------------
    # Expressões finais
    # ----------------------------
    custo_hora_expr = cast(func.coalesce(DimProjeto.custo_hora, 0), Numeric(12, 2))
    total_horas_expr = cast(
        func.coalesce(horas_subquery.c.total_horas, 0),
        Numeric(12, 2),
    )
    custo_materiais_expr = cast(
        func.coalesce(materiais_subquery.c.custo_materiais, 0),
        Numeric(12, 2),
    )

    custo_horas_expr = cast(
        total_horas_expr * custo_hora_expr,
        Numeric(12, 2),
    )

    custo_total_expr = cast(
        custo_materiais_expr + custo_horas_expr,
        Numeric(12, 2),
    )

    # Flags úteis para debug/ETL
    custo_hora_zerado_expr = case(
        (func.coalesce(DimProjeto.custo_hora, 0) == 0, literal(True)),
        else_=literal(False),
    ).label("custo_hora_zerado")

    base_query = (
        db.query(
            DimProjeto.id_projeto.label("id_projeto"),
            DimProjeto.codigo_projeto.label("codigo_projeto"),
            DimProjeto.nome_projeto.label("nome_projeto"),
            DimProjeto.responsavel.label("responsavel"),
            DimProjeto.status.label("status"),
            custo_hora_expr.label("custo_hora"),
            total_horas_expr.label("total_horas"),
            custo_materiais_expr.label("custo_materiais"),
            custo_horas_expr.label("custo_horas"),
            custo_total_expr.label("custo_total"),
            custo_hora_zerado_expr,
        )
        .outerjoin(
            materiais_subquery,
            DimProjeto.id_projeto == materiais_subquery.c.projeto_id,
        )
        .outerjoin(
            horas_subquery,
            DimProjeto.id_projeto == horas_subquery.c.projeto_id,
        )
    )

    return base_query


@router.get("", response_model=DashboardResumoResponse)
async def get_dashboard_root(
    data_inicio: date | None = Query(default=None),
    data_fim: date | None = Query(default=None),
    db: Session = Depends(get_db),
):
    return await get_dashboard_resumo(
        data_inicio=data_inicio,
        data_fim=data_fim,
        db=db,
    )


@router.get("/projetos", response_model=list[DashboardProjetoResponse])
async def get_dashboard_projetos(
    data_inicio: date | None = Query(default=None),
    data_fim: date | None = Query(default=None),
    db: Session = Depends(get_db),
):
    resultados = (
        _build_dashboard_cost_query(
            db=db,
            data_inicio=data_inicio,
            data_fim=data_fim,
        )
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
            custo_hora=_safe_decimal(row.custo_hora),
            total_horas=_safe_decimal(row.total_horas),
            custo_materiais=_safe_decimal(row.custo_materiais),
            custo_horas=_safe_decimal(row.custo_horas),
            custo_total=_safe_decimal(row.custo_total),
        )
        for row in resultados
    ]


@router.get("/resumo", response_model=DashboardResumoResponse)
async def get_dashboard_resumo(
    data_inicio: date | None = Query(default=None),
    data_fim: date | None = Query(default=None),
    db: Session = Depends(get_db),
):
    base_subquery = _build_dashboard_cost_query(
        db=db,
        data_inicio=data_inicio,
        data_fim=data_fim,
    ).subquery()

    resultado = db.query(
        func.count(base_subquery.c.id_projeto).label("total_projetos"),
        cast(
            func.coalesce(func.sum(base_subquery.c.custo_materiais), 0),
            Numeric(14, 2),
        ).label("custo_materiais_geral"),
        cast(
            func.coalesce(func.sum(base_subquery.c.total_horas), 0),
            Numeric(14, 2),
        ).label("total_horas_geral"),
        cast(
            func.coalesce(func.sum(base_subquery.c.custo_horas), 0),
            Numeric(14, 2),
        ).label("custo_horas_geral"),
        cast(
            func.coalesce(func.sum(base_subquery.c.custo_total), 0),
            Numeric(14, 2),
        ).label("custo_total_geral"),
        cast(
            func.coalesce(func.avg(base_subquery.c.custo_total), 0),
            Numeric(14, 2),
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
