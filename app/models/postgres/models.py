from sqlalchemy import Column, Date, Integer, Numeric, String

from app.db.database import Base

SCHEMA = "dw"


class DimPrograma(Base):
    __tablename__ = "dim_programa"
    __table_args__ = {"schema": SCHEMA}

    programa_key = Column(Integer, primary_key=True, index=True)
    programa_orig_id = Column(Integer)
    codigo_programa = Column(String)
    nome_programa = Column(String)
    gerente_programa = Column(String)
    gerente_tecnico = Column(String)
    data_inicio = Column(Date)
    data_fim_prevista = Column(Date)
    status = Column(String)


class DimProjeto(Base):
    __tablename__ = "dim_projeto"
    __table_args__ = {"schema": SCHEMA}

    projeto_key = Column(Integer, primary_key=True, index=True)
    projeto_orig_id = Column(Integer)
    programa_key = Column(Integer)
    codigo_projeto = Column(String)
    nome_projeto = Column(String)
    responsavel = Column(String)
    custo_hora = Column(Numeric)
    data_inicio = Column(Date)
    data_fim_prevista = Column(Date)
    status = Column(String)


class DimTarefa(Base):
    __tablename__ = "dim_tarefa"
    __table_args__ = {"schema": SCHEMA}

    tarefa_key = Column(Integer, primary_key=True, index=True)
    tarefa_orig_id = Column(Integer)
    projeto_key = Column(Integer)
    codigo_tarefa = Column(String)
    titulo = Column(String)
    responsavel = Column(String)
    estimativa_horas = Column(Numeric)
    data_inicio = Column(Date)
    data_fim_prevista = Column(Date)
    status = Column(String)


class DimMaterial(Base):
    __tablename__ = "dim_material"
    __table_args__ = {"schema": SCHEMA}

    material_key = Column(Integer, primary_key=True, index=True)
    material_orig_id = Column(Integer)
    codigo_material = Column(String)
    descricao = Column(String)
    categoria = Column(String)
    fabricante = Column(String)
    custo_estimado = Column(Numeric)
    status = Column(String)


class DimFornecedor(Base):
    __tablename__ = "dim_fornecedor"
    __table_args__ = {"schema": SCHEMA}

    fornecedor_key = Column(Integer, primary_key=True, index=True)
    fornecedor_orig_id = Column(Integer)
    codigo_fornecedor = Column(String)
    razao_social = Column(String)
    cidade = Column(String)
    estado = Column(String)
    categoria = Column(String)
    status = Column(String)


class DimUsuario(Base):
    __tablename__ = "dim_usuario"
    __table_args__ = {"schema": SCHEMA}

    usuario_key = Column(Integer, primary_key=True, index=True)
    nome_usuario = Column(String)


class DimLocalizacao(Base):
    __tablename__ = "dim_localizacao"
    __table_args__ = {"schema": SCHEMA}

    localizacao_key = Column(Integer, primary_key=True, index=True)
    localizacao = Column(String)


class DimData(Base):
    __tablename__ = "dim_data"
    __table_args__ = {"schema": SCHEMA}

    data_key = Column(Integer, primary_key=True, index=True)
    data = Column(Date)
    ano = Column(Integer)
    mes = Column(Integer)
    dia = Column(Integer)
    trimestre = Column(Integer)
    nome_mes = Column(String)
    dia_semana = Column(Integer)


class FatoHorasTrabalhadas(Base):
    __tablename__ = "fato_horas_trabalhadas"
    __table_args__ = {"schema": SCHEMA}

    fato_horas_key = Column(Integer, primary_key=True, index=True)
    horas_trabalhadas_orig_id = Column(Integer)
    tarefa_key = Column(Integer)
    usuario_key = Column(Integer)
    data_key = Column(Integer)
    horas_trabalhadas = Column(Numeric)


class FatoSolicitacoesCompra(Base):
    __tablename__ = "fato_solicitacoes_compra"
    __table_args__ = {"schema": SCHEMA}

    fato_solicitacao_key = Column(Integer, primary_key=True, index=True)
    solicitacao_orig_id = Column(Integer)
    numero_solicitacao = Column(String)
    projeto_key = Column(Integer)
    material_key = Column(Integer)
    data_key = Column(Integer)
    quantidade = Column(Numeric)
    prioridade = Column(String)
    status = Column(String)


class FatoPedidosCompra(Base):
    __tablename__ = "fato_pedidos_compra"
    __table_args__ = {"schema": SCHEMA}

    fato_pedido_key = Column(Integer, primary_key=True, index=True)
    pedido_compra_orig_id = Column(Integer)
    numero_pedido = Column(String)
    solicitacao_id = Column(Integer)
    projeto_id = Column(Integer)
    material_id = Column(Integer)
    fornecedor_key = Column(Integer)
    data_pedido_key = Column(Integer)
    data_previsao_key = Column(Integer)
    valor_total = Column(Numeric)
    status = Column(String)


class FatoComprasProjeto(Base):
    __tablename__ = "fato_compras_projeto"
    __table_args__ = {"schema": SCHEMA}

    fato_compra_projeto_key = Column(Integer, primary_key=True, index=True)
    compra_projeto_orig_id = Column(Integer)
    pedido_compra_id = Column(Integer)
    projeto_key = Column(Integer)
    valor_alocado = Column(Numeric)


class FatoEmpenhoMateriais(Base):
    __tablename__ = "fato_empenho_materiais"
    __table_args__ = {"schema": SCHEMA}

    fato_empenho_key = Column(Integer, primary_key=True, index=True)
    empenho_material_orig_id = Column(Integer)
    projeto_key = Column(Integer)
    material_key = Column(Integer)
    data_key = Column(Integer)
    quantidade_empenhada = Column(Numeric)


class FatoEstoqueMateriaisProjeto(Base):
    __tablename__ = "fato_estoque_materiais_projeto"
    __table_args__ = {"schema": SCHEMA}

    fato_estoque_key = Column(Integer, primary_key=True, index=True)
    estoque_material_projeto_orig_id = Column(Integer)
    projeto_key = Column(Integer)
    material_key = Column(Integer)
    localizacao_key = Column(Integer)
    quantidade = Column(Numeric)
