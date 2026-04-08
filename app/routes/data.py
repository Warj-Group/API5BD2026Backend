from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.postgres.models import (
    DimData,
    DimFornecedor,
    DimLocalizacao,
    DimMaterial,
    DimPrograma,
    DimProjeto,
    DimTarefa,
    DimUsuario,
    FatoComprasProjeto,
    FatoEmpenhoMateriais,
    FatoEstoqueMateriaisProjeto,
    FatoHorasTrabalhadas,
    FatoPedidosCompra,
    FatoSolicitacoesCompra,
)
from app.schemas.dashboard import (
    DataOut,
    FornecedorOut,
    FatoComprasProjetoOut,
    FatoEmpenhoMateriaisOut,
    FatoEstoqueMateriaisProjetoOut,
    FatoHorasTrabalhadasOut,
    FatoPedidosCompraOut,
    FatoSolicitacoesCompraOut,
    LocalizacaoOut,
    MaterialOut,
    ProgramaOut,
    ProjetoOut,
    TarefaOut,
    UsuarioOut,
)

router = APIRouter(prefix="/data", tags=["data"])


@router.get("/programas", response_model=list[ProgramaOut])
def get_programas(
    db: Session = Depends(get_db),
    codigo: Optional[str] = None,
    nome: Optional[str] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = Query(100, le=1000),
):
    query = db.query(DimPrograma)
    if codigo:
        query = query.filter(DimPrograma.codigo_programa.ilike(f"%{codigo}%"))
    if nome:
        query = query.filter(DimPrograma.nome_programa.ilike(f"%{nome}%"))
    if status:
        query = query.filter(DimPrograma.status.ilike(f"%{status}%"))
    return query.order_by(DimPrograma.programa_key.asc()).offset(skip).limit(limit).all()


@router.get("/projetos", response_model=list[ProjetoOut])
def get_projetos(
    db: Session = Depends(get_db),
    programa_key: Optional[int] = None,
    responsavel: Optional[str] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = Query(100, le=1000),
):
    query = db.query(DimProjeto)
    if programa_key is not None:
        query = query.filter(DimProjeto.programa_key == programa_key)
    if responsavel:
        query = query.filter(DimProjeto.responsavel.ilike(f"%{responsavel}%"))
    if status:
        query = query.filter(DimProjeto.status.ilike(f"%{status}%"))
    return query.order_by(DimProjeto.projeto_key.asc()).offset(skip).limit(limit).all()


@router.get("/tarefas", response_model=list[TarefaOut])
def get_tarefas(
    db: Session = Depends(get_db),
    projeto_key: Optional[int] = None,
    responsavel: Optional[str] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = Query(100, le=1000),
):
    query = db.query(DimTarefa)
    if projeto_key is not None:
        query = query.filter(DimTarefa.projeto_key == projeto_key)
    if responsavel:
        query = query.filter(DimTarefa.responsavel.ilike(f"%{responsavel}%"))
    if status:
        query = query.filter(DimTarefa.status.ilike(f"%{status}%"))
    return query.order_by(DimTarefa.tarefa_key.asc()).offset(skip).limit(limit).all()


@router.get("/materiais", response_model=list[MaterialOut])
def get_materiais(
    db: Session = Depends(get_db),
    categoria: Optional[str] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = Query(100, le=1000),
):
    query = db.query(DimMaterial)
    if categoria:
        query = query.filter(DimMaterial.categoria.ilike(f"%{categoria}%"))
    if status:
        query = query.filter(DimMaterial.status.ilike(f"%{status}%"))
    return query.order_by(DimMaterial.material_key.asc()).offset(skip).limit(limit).all()


@router.get("/fornecedores", response_model=list[FornecedorOut])
def get_fornecedores(
    db: Session = Depends(get_db),
    cidade: Optional[str] = None,
    estado: Optional[str] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = Query(100, le=1000),
):
    query = db.query(DimFornecedor)
    if cidade:
        query = query.filter(DimFornecedor.cidade.ilike(f"%{cidade}%"))
    if estado:
        query = query.filter(DimFornecedor.estado.ilike(f"%{estado}%"))
    if status:
        query = query.filter(DimFornecedor.status.ilike(f"%{status}%"))
    return query.order_by(DimFornecedor.fornecedor_key.asc()).offset(skip).limit(limit).all()


@router.get("/usuarios", response_model=list[UsuarioOut])
def get_usuarios(
    db: Session = Depends(get_db),
    nome: Optional[str] = None,
    skip: int = 0,
    limit: int = Query(100, le=1000),
):
    query = db.query(DimUsuario)
    if nome:
        query = query.filter(DimUsuario.nome_usuario.ilike(f"%{nome}%"))
    return query.order_by(DimUsuario.usuario_key.asc()).offset(skip).limit(limit).all()


@router.get("/localizacoes", response_model=list[LocalizacaoOut])
def get_localizacoes(
    db: Session = Depends(get_db),
    nome: Optional[str] = None,
    skip: int = 0,
    limit: int = Query(100, le=1000),
):
    query = db.query(DimLocalizacao)
    if nome:
        query = query.filter(DimLocalizacao.localizacao.ilike(f"%{nome}%"))
    return query.order_by(DimLocalizacao.localizacao_key.asc()).offset(skip).limit(limit).all()


@router.get("/datas", response_model=list[DataOut])
def get_datas(
    db: Session = Depends(get_db),
    ano: Optional[int] = None,
    mes: Optional[int] = None,
    skip: int = 0,
    limit: int = Query(100, le=1000),
):
    query = db.query(DimData)
    if ano is not None:
        query = query.filter(DimData.ano == ano)
    if mes is not None:
        query = query.filter(DimData.mes == mes)
    return query.order_by(DimData.data.asc()).offset(skip).limit(limit).all()


@router.get("/fato-horas-trabalhadas", response_model=list[FatoHorasTrabalhadasOut])
def get_fato_horas_trabalhadas(
    db: Session = Depends(get_db),
    tarefa_key: Optional[int] = None,
    usuario_key: Optional[int] = None,
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    skip: int = 0,
    limit: int = Query(100, le=1000),
):
    query = db.query(FatoHorasTrabalhadas).join(DimData, FatoHorasTrabalhadas.data_key == DimData.data_key)
    if tarefa_key is not None:
        query = query.filter(FatoHorasTrabalhadas.tarefa_key == tarefa_key)
    if usuario_key is not None:
        query = query.filter(FatoHorasTrabalhadas.usuario_key == usuario_key)
    if data_inicio is not None:
        query = query.filter(DimData.data >= data_inicio)
    if data_fim is not None:
        query = query.filter(DimData.data <= data_fim)
    return query.order_by(FatoHorasTrabalhadas.fato_horas_key.asc()).offset(skip).limit(limit).all()


@router.get("/fato-solicitacoes-compra", response_model=list[FatoSolicitacoesCompraOut])
def get_fato_solicitacoes_compra(
    db: Session = Depends(get_db),
    projeto_key: Optional[int] = None,
    material_key: Optional[int] = None,
    status: Optional[str] = None,
    prioridade: Optional[str] = None,
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    skip: int = 0,
    limit: int = Query(100, le=1000),
):
    query = db.query(FatoSolicitacoesCompra).join(DimData, FatoSolicitacoesCompra.data_key == DimData.data_key)
    if projeto_key is not None:
        query = query.filter(FatoSolicitacoesCompra.projeto_key == projeto_key)
    if material_key is not None:
        query = query.filter(FatoSolicitacoesCompra.material_key == material_key)
    if status:
        query = query.filter(FatoSolicitacoesCompra.status.ilike(f"%{status}%"))
    if prioridade:
        query = query.filter(FatoSolicitacoesCompra.prioridade.ilike(f"%{prioridade}%"))
    if data_inicio is not None:
        query = query.filter(DimData.data >= data_inicio)
    if data_fim is not None:
        query = query.filter(DimData.data <= data_fim)
    return query.order_by(FatoSolicitacoesCompra.fato_solicitacao_key.asc()).offset(skip).limit(limit).all()


@router.get("/fato-pedidos-compra", response_model=list[FatoPedidosCompraOut])
def get_fato_pedidos_compra(
    db: Session = Depends(get_db),
    fornecedor_key: Optional[int] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = Query(100, le=1000),
):
    query = db.query(FatoPedidosCompra)
    if fornecedor_key is not None:
        query = query.filter(FatoPedidosCompra.fornecedor_key == fornecedor_key)
    if status:
        query = query.filter(FatoPedidosCompra.status.ilike(f"%{status}%"))
    return query.order_by(FatoPedidosCompra.fato_pedido_key.asc()).offset(skip).limit(limit).all()


@router.get("/fato-compras-projeto", response_model=list[FatoComprasProjetoOut])
def get_fato_compras_projeto(
    db: Session = Depends(get_db),
    projeto_key: Optional[int] = None,
    skip: int = 0,
    limit: int = Query(100, le=1000),
):
    query = db.query(FatoComprasProjeto)
    if projeto_key is not None:
        query = query.filter(FatoComprasProjeto.projeto_key == projeto_key)
    return query.order_by(FatoComprasProjeto.fato_compra_projeto_key.asc()).offset(skip).limit(limit).all()


@router.get("/fato-empenho-materiais", response_model=list[FatoEmpenhoMateriaisOut])
def get_fato_empenho_materiais(
    db: Session = Depends(get_db),
    projeto_key: Optional[int] = None,
    material_key: Optional[int] = None,
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    skip: int = 0,
    limit: int = Query(100, le=1000),
):
    query = db.query(FatoEmpenhoMateriais).join(DimData, FatoEmpenhoMateriais.data_key == DimData.data_key)
    if projeto_key is not None:
        query = query.filter(FatoEmpenhoMateriais.projeto_key == projeto_key)
    if material_key is not None:
        query = query.filter(FatoEmpenhoMateriais.material_key == material_key)
    if data_inicio is not None:
        query = query.filter(DimData.data >= data_inicio)
    if data_fim is not None:
        query = query.filter(DimData.data <= data_fim)
    return query.order_by(FatoEmpenhoMateriais.fato_empenho_key.asc()).offset(skip).limit(limit).all()


@router.get("/fato-estoque-materiais", response_model=list[FatoEstoqueMateriaisProjetoOut])
def get_fato_estoque_materiais(
    db: Session = Depends(get_db),
    projeto_key: Optional[int] = None,
    material_key: Optional[int] = None,
    localizacao_key: Optional[int] = None,
    skip: int = 0,
    limit: int = Query(100, le=1000),
):
    query = db.query(FatoEstoqueMateriaisProjeto)
    if projeto_key is not None:
        query = query.filter(FatoEstoqueMateriaisProjeto.projeto_key == projeto_key)
    if material_key is not None:
        query = query.filter(FatoEstoqueMateriaisProjeto.material_key == material_key)
    if localizacao_key is not None:
        query = query.filter(FatoEstoqueMateriaisProjeto.localizacao_key == localizacao_key)
    return query.order_by(FatoEstoqueMateriaisProjeto.fato_estoque_key.asc()).offset(skip).limit(limit).all()
