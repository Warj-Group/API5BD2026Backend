from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ProgramaOut(BaseModel):
    programa_key: int
    programa_orig_id: Optional[int] = None
    codigo_programa: Optional[str] = None
    nome_programa: Optional[str] = None
    gerente_programa: Optional[str] = None
    gerente_tecnico: Optional[str] = None
    data_inicio: Optional[date] = None
    data_fim_prevista: Optional[date] = None
    status: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class ProjetoOut(BaseModel):
    projeto_key: int
    projeto_orig_id: Optional[int] = None
    programa_key: Optional[int] = None
    codigo_projeto: Optional[str] = None
    nome_projeto: Optional[str] = None
    responsavel: Optional[str] = None
    custo_hora: Optional[Decimal] = None
    data_inicio: Optional[date] = None
    data_fim_prevista: Optional[date] = None
    status: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class TarefaOut(BaseModel):
    tarefa_key: int
    tarefa_orig_id: Optional[int] = None
    projeto_key: Optional[int] = None
    codigo_tarefa: Optional[str] = None
    titulo: Optional[str] = None
    responsavel: Optional[str] = None
    estimativa_horas: Optional[Decimal] = None
    data_inicio: Optional[date] = None
    data_fim_prevista: Optional[date] = None
    status: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class MaterialOut(BaseModel):
    material_key: int
    material_orig_id: Optional[int] = None
    codigo_material: Optional[str] = None
    descricao: Optional[str] = None
    categoria: Optional[str] = None
    fabricante: Optional[str] = None
    custo_estimado: Optional[Decimal] = None
    status: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class FornecedorOut(BaseModel):
    fornecedor_key: int
    fornecedor_orig_id: Optional[int] = None
    codigo_fornecedor: Optional[str] = None
    razao_social: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    categoria: Optional[str] = None
    status: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class UsuarioOut(BaseModel):
    usuario_key: int
    nome_usuario: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class LocalizacaoOut(BaseModel):
    localizacao_key: int
    localizacao: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class DataOut(BaseModel):
    data_key: int
    data: Optional[date] = None
    ano: Optional[int] = None
    mes: Optional[int] = None
    dia: Optional[int] = None
    trimestre: Optional[int] = None
    nome_mes: Optional[str] = None
    dia_semana: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)


class FatoHorasTrabalhadasOut(BaseModel):
    fato_horas_key: int
    horas_trabalhadas_orig_id: Optional[int] = None
    tarefa_key: Optional[int] = None
    usuario_key: Optional[int] = None
    data_key: Optional[int] = None
    horas_trabalhadas: Optional[Decimal] = None
    model_config = ConfigDict(from_attributes=True)


class FatoSolicitacoesCompraOut(BaseModel):
    fato_solicitacao_key: int
    solicitacao_orig_id: Optional[int] = None
    numero_solicitacao: Optional[str] = None
    projeto_key: Optional[int] = None
    material_key: Optional[int] = None
    data_key: Optional[int] = None
    quantidade: Optional[Decimal] = None
    prioridade: Optional[str] = None
    status: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class FatoPedidosCompraOut(BaseModel):
    fato_pedido_key: int
    pedido_compra_orig_id: Optional[int] = None
    numero_pedido: Optional[str] = None
    solicitacao_id: Optional[int] = None
    projeto_id: Optional[int] = None
    material_id: Optional[int] = None
    fornecedor_key: Optional[int] = None
    data_pedido_key: Optional[int] = None
    data_previsao_key: Optional[int] = None
    valor_total: Optional[Decimal] = None
    status: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class FatoComprasProjetoOut(BaseModel):
    fato_compra_projeto_key: int
    compra_projeto_orig_id: Optional[int] = None
    pedido_compra_id: Optional[int] = None
    projeto_key: Optional[int] = None
    valor_alocado: Optional[Decimal] = None
    model_config = ConfigDict(from_attributes=True)


class FatoEmpenhoMateriaisOut(BaseModel):
    fato_empenho_key: int
    empenho_material_orig_id: Optional[int] = None
    projeto_key: Optional[int] = None
    material_key: Optional[int] = None
    data_key: Optional[int] = None
    quantidade_empenhada: Optional[Decimal] = None
    model_config = ConfigDict(from_attributes=True)


class FatoEstoqueMateriaisProjetoOut(BaseModel):
    fato_estoque_key: int
    estoque_material_projeto_orig_id: Optional[int] = None
    projeto_key: Optional[int] = None
    material_key: Optional[int] = None
    localizacao_key: Optional[int] = None
    quantidade: Optional[Decimal] = None
    model_config = ConfigDict(from_attributes=True)
