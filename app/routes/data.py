from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.postgres.models import (
    DimData,
    DimFornecedor,
    DimMaterial,
    DimPedidoCompra,
    DimPrograma,
    DimProjeto,
    DimTarefa,
    DimUsuario,
    FactCompras,
    FactConsumoMateriais,
    FactHorasTrabalhadas,
)

router = APIRouter(prefix="/data", tags=["data"])


@router.get("/programas", response_model=List[dict])
def get_programas(db: Session = Depends(get_db)):
    programas = db.query(DimPrograma).all()
    return [
        {
            "id": p.id_programa,
            "codigo_programa": p.codigo_programa,
            "nome_programa": p.nome_programa,
            "gerente_programa": p.gerente_programa,
            "gerente_tecnico": p.gerente_tecnico,
        }
        for p in programas
    ]


@router.get("/projetos", response_model=List[dict])
def get_projetos(db: Session = Depends(get_db)):
    projetos = db.query(DimProjeto).all()
    return [
        {
            "id": p.id_projeto,
            "codigo_projeto": p.codigo_projeto,
            "nome_projeto": p.nome_projeto,
            "programa_id": p.programa_id,
            "responsavel": p.responsavel,
        }
        for p in projetos
    ]


@router.get("/materiais", response_model=List[dict])
def get_materiais(db: Session = Depends(get_db)):
    materiais = db.query(DimMaterial).all()
    return [
        {
            "id": m.id_material,
            "codigo_material": m.codigo_material,
            "descricao": m.descricao,
            "categoria": m.categoria,
            "fabricante": m.fabricante,
        }
        for m in materiais
    ]


@router.get("/fornecedores", response_model=List[dict])
def get_fornecedores(db: Session = Depends(get_db)):
    fornecedores = db.query(DimFornecedor).all()
    return [
        {
            "id": f.id_fornecedor,
            "codigo_fornecedor": f.codigo_fornecedor,
            "razao_social": f.razao_social,
            "cidade": f.cidade,
            "estado": f.estado,
        }
        for f in fornecedores
    ]


@router.get("/usuarios", response_model=List[dict])
def get_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(DimUsuario).all()
    return [{"id": u.id_usuario, "nome_usuario": u.nome_usuario} for u in usuarios]


@router.get("/tarefas", response_model=List[dict])
def get_tarefas(db: Session = Depends(get_db)):
    tarefas = db.query(DimTarefa).all()
    return [
        {
            "id": t.id_tarefa,
            "codigo": t.codigo_tarefa,
            "titulo": t.titulo,
            "estimativa_horas": t.estimativa_horas,
            "status": t.status,
        }
        for t in tarefas
    ]


@router.get("/datas", response_model=List[dict])
def get_datas(db: Session = Depends(get_db)):
    datas = db.query(DimData).all()
    return [
        {
            "id": d.id_data,
            "data": d.data,
            "dia": d.dia,
            "mes": d.mes,
            "nome_mes": d.nome_mes,
            "nome_dia_semana": d.nome_dia_semana,
        }
        for d in datas
    ]


@router.get("/pedidos-compra", response_model=List[dict])
def get_pedidos_compra(db: Session = Depends(get_db)):
    pedidos = db.query(DimPedidoCompra).all()
    return [
        {
            "id": p.id_pedido,
            "numero_pedido": p.numero_pedido,
            "fornecedor_id": p.fornecedor_id,
            "data_pedido": p.data_pedido,
            "data_previsao_entrega": p.data_previsao_entrega,
            "status": p.status,
        }
        for p in pedidos
    ]


@router.get("/consumo-materiais", response_model=List[dict])
def get_consumo_materiais(db: Session = Depends(get_db)):
    consumos = db.query(FactConsumoMateriais).all()
    return [
        {
            "id": c.id_fato_material,
            "projeto_id": c.projeto_id,
            "material_id": c.material_id,
            "fornecedor_id": c.fornecedor_id,
            "data_id": c.data_id,
            "quantidade_empenhada": c.quantidade_empenhada,
            "custo_unitario": float(c.custo_unitario)
            if c.custo_unitario is not None
            else None,
            "custo_total": float(c.custo_total) if c.custo_total is not None else None,
        }
        for c in consumos
    ]


@router.get("/horas-trabalhadas", response_model=List[dict])
def get_horas_trabalhadas(db: Session = Depends(get_db)):
    horas = db.query(FactHorasTrabalhadas).all()
    return [
        {
            "id": h.id_fato_horas,
            "programa_id": h.programa_id,
            "projeto_id": h.projeto_id,
            "tarefa_id": h.tarefa_id,
            "usuario_id": h.usuario_id,
            "data_id": h.data_id,
            "horas_trabalhadas": float(h.horas_trabalhadas)
            if h.horas_trabalhadas is not None
            else None,
            "custo_hora": float(h.custo_hora) if h.custo_hora is not None else None,
            "custo_total": float(h.custo_total) if h.custo_total is not None else None,
        }
        for h in horas
    ]


@router.get("/compras", response_model=List[dict])
def get_compras(db: Session = Depends(get_db)):
    compras = db.query(FactCompras).all()
    return [
        {
            "id": c.id_fato_compra,
            "pedido_id": c.pedido_id,
            "projeto_id": c.projeto_id,
            "fornecedor_id": c.fornecedor_id,
            "data_id": c.data_id,
            "valor_total": float(c.valor_total) if c.valor_total is not None else None,
        }
        for c in compras
    ]
