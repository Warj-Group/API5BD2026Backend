from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.models.postgres.models import (
    DimPrograma, DimProjeto, DimMaterial, DimFornecedor,
    DimUsuario, DimTarefa, DimData,
    FactConsumoMateriais, FactHorasTrabalhadas
)

router = APIRouter(prefix="/data", tags=["data"])

@router.get("/programas", response_model=List[dict])
def get_programas(db: Session = Depends(get_db)):
    programas = db.query(DimPrograma).all()
    return [{"id": p.id_programa, "codigo": p.codigo_programa, "nome": p.nome_programa, "gerente": p.gerente_programa, "status": p.status} for p in programas]

@router.get("/projetos", response_model=List[dict])
def get_projetos(db: Session = Depends(get_db)):
    projetos = db.query(DimProjeto).all()
    return [{"id": p.id_projeto, "codigo": p.codigo_projeto, "nome": p.nome_projeto, "responsavel": p.responsavel, "data_inicio": p.data_inicio, "status": p.status} for p in projetos]

@router.get("/materiais", response_model=List[dict])
def get_materiais(db: Session = Depends(get_db)):
    materiais = db.query(DimMaterial).all()
    return [{"id": m.id_material, "codigo": m.codigo_material, "categoria": m.categoria, "descricao": m.descricao, "fabricante": m.fabricante, "unidade_medida": m.unidade_medida, "lead_time_dias": m.lead_time_dias, "custo_estimado": m.custo_estimado} for m in materiais]

@router.get("/fornecedores", response_model=List[dict])
def get_fornecedores(db: Session = Depends(get_db)):
    fornecedores = db.query(DimFornecedor).all()
    return [{"id": f.id_fornecedor, "razao_social": f.razao_social, "nome_fantasia": f.nome_fantasia, "cidade": f.cidade, "estado": f.estado, "email": f.email, "telefone": f.telefone, "categoria_fornecedor": f.categoria_fornecedor, "cnpj": f.cnpj, "condicao_pagamento": f.condicao_pagamento, "status": f.status, "data_cadastro": f.data_cadastro} for f in fornecedores]

@router.get("/usuarios", response_model=List[dict])
def get_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(DimUsuario).all()
    return [{"id": u.id_usuario, "nome": u.nome_usuario, "departamento": u.departamento} for u in usuarios]

@router.get("/tarefas", response_model=List[dict])
def get_tarefas(db: Session = Depends(get_db)):
    tarefas = db.query(DimTarefa).all()
    return [{"id": t.id_tarefa, "codigo": t.codigo_tarefa, "titulo": t.titulo, "estimativa_horas": t.estimativa_horas, "status": t.status} for t in tarefas]

@router.get("/datas", response_model=List[dict])
def get_datas(db: Session = Depends(get_db)):
    datas = db.query(DimData).all()
    return [{"id": d.id_data, "data": d.data, "dia": d.dia, "mes": d.mes, "trimestre": d.trimestre, "ano": d.ano} for d in datas]

@router.get("/consumo-materiais", response_model=List[dict])
def get_consumo_materiais(db: Session = Depends(get_db)):
    consumos = db.query(FactConsumoMateriais).all()
    return [{"id": c.id_fato_material, "programa_id": c.programa_id, "projeto_id": c.projeto_id, "material_id": c.material_id, "fornecedor_id": c.fornecedor_id, "data_id": c.data_id, "quantidade_empenhada": c.quantidade_empenhada, "custo_unitario": c.custo_unitario, "custo_total": c.custo_total} for c in consumos]

@router.get("/horas-trabalhadas", response_model=List[dict])
def get_horas_trabalhadas(db: Session = Depends(get_db)):
    horas = db.query(FactHorasTrabalhadas).all()
    return [{"id": h.id_fato_horas, "programa_id": h.programa_id, "projeto_id": h.projeto_id, "tarefa_id": h.tarefa_id, "usuario_id": h.usuario_id, "data_id": h.data_id, "horas_trabalhadas": h.horas_trabalhadas, "custo_hora": h.custo_hora, "custo_total_hora": h.custo_total_hora} for h in horas]