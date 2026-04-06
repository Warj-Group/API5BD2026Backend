from sqlalchemy import Column, Date, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship

from app.db.database import Base


class DimPrograma(Base):
    __tablename__ = "dim_programa"
    __table_args__ = {"schema": "dw_projeto"}

    id_programa = Column(Integer, primary_key=True, index=True)
    codigo_programa = Column(String(20), unique=True, nullable=False)
    nome_programa = Column(String(200), nullable=True)
    gerente_programa = Column(String(100), nullable=True)
    gerente_tecnico = Column(String(100), nullable=True)
    data_inicio = Column(Date, nullable=True)
    data_fim_prevista = Column(Date, nullable=True)
    status = Column(String(20), nullable=True)

    projetos = relationship("DimProjeto", back_populates="programa")
    horas_trabalhadas = relationship("FactHorasTrabalhadas", back_populates="programa")
    consumo_materiais = relationship("FactConsumoMateriais", back_populates="programa")
    compras = relationship("FactCompras", back_populates="programa")


class DimProjeto(Base):
    __tablename__ = "dim_projeto"
    __table_args__ = {"schema": "dw_projeto"}

    id_projeto = Column(Integer, primary_key=True, index=True)
    codigo_projeto = Column(String(20), unique=True, nullable=False)
    nome_projeto = Column(String(200), nullable=True)
    programa_id = Column(
        Integer,
        ForeignKey("dw_projeto.dim_programa.id_programa"),
        nullable=True,
    )
    responsavel = Column(String(100), nullable=True)
    custo_hora = Column(Numeric(10, 2), nullable=True)
    data_inicio = Column(Date, nullable=True)
    data_fim_prevista = Column(Date, nullable=True)
    status = Column(String(20), nullable=True)

    programa = relationship("DimPrograma", back_populates="projetos")
    tarefas = relationship("DimTarefa", back_populates="projeto")
    horas_trabalhadas = relationship("FactHorasTrabalhadas", back_populates="projeto")
    consumo_materiais = relationship("FactConsumoMateriais", back_populates="projeto")
    compras = relationship("FactCompras", back_populates="projeto")


class DimMaterial(Base):
    __tablename__ = "dim_material"
    __table_args__ = {"schema": "dw_projeto"}

    id_material = Column(Integer, primary_key=True, index=True)
    codigo_material = Column(String(50), unique=True, nullable=False)
    descricao = Column(Text, nullable=True)
    categoria = Column(String(100), nullable=True)
    fabricante = Column(String(100), nullable=True)
    custo_estimado = Column(Numeric(10, 2), nullable=True)
    status = Column(String(20), nullable=True)

    consumo_materiais = relationship("FactConsumoMateriais", back_populates="material")


class DimFornecedor(Base):
    __tablename__ = "dim_fornecedor"
    __table_args__ = {"schema": "dw_projeto"}

    id_fornecedor = Column(Integer, primary_key=True, index=True)
    codigo_fornecedor = Column(String(20), unique=True, nullable=False)
    razao_social = Column(String(200), nullable=True)
    cidade = Column(String(100), nullable=True)
    estado = Column(String(50), nullable=True)
    categoria = Column(String(100), nullable=True)
    status = Column(String(20), nullable=True)

    pedidos_compra = relationship("DimPedidoCompra", back_populates="fornecedor")
    consumo_materiais = relationship(
        "FactConsumoMateriais", back_populates="fornecedor"
    )
    compras = relationship("FactCompras", back_populates="fornecedor")


class DimUsuario(Base):
    __tablename__ = "dim_usuario"
    __table_args__ = {"schema": "dw_projeto"}

    id_usuario = Column(Integer, primary_key=True, index=True)
    nome_usuario = Column(String(100), unique=True, nullable=False)

    horas_trabalhadas = relationship("FactHorasTrabalhadas", back_populates="usuario")


class DimTarefa(Base):
    __tablename__ = "dim_tarefa"
    __table_args__ = {"schema": "dw_projeto"}

    id_tarefa = Column(Integer, primary_key=True, index=True)
    codigo_tarefa = Column(String(20), unique=True, nullable=False)
    projeto_id = Column(
        Integer,
        ForeignKey("dw_projeto.dim_projeto.id_projeto"),
        nullable=True,
    )
    titulo = Column(String(200), nullable=True)
    responsavel = Column(String(100), nullable=True)
    estimativa_horas = Column(Integer, nullable=True)
    data_inicio = Column(Date, nullable=True)
    data_fim_prevista = Column(Date, nullable=True)
    status = Column(String(20), nullable=True)

    projeto = relationship("DimProjeto", back_populates="tarefas")
    horas_trabalhadas = relationship("FactHorasTrabalhadas", back_populates="tarefa")


class DimData(Base):
    __tablename__ = "dim_data"
    __table_args__ = {"schema": "dw_projeto"}

    id_data = Column(Integer, primary_key=True, index=True)
    data = Column(Date, unique=True, nullable=False)
    dia = Column(Integer, nullable=True)
    mes = Column(Integer, nullable=True)
    nome_mes = Column(String(20), nullable=True)
    trimestre = Column(Integer, nullable=True)
    ano = Column(Integer, nullable=True)
    dia_semana = Column(Integer, nullable=True)
    nome_dia_semana = Column(String(20), nullable=True)

    horas_trabalhadas = relationship("FactHorasTrabalhadas", back_populates="data")
    consumo_materiais = relationship("FactConsumoMateriais", back_populates="data")
    compras = relationship("FactCompras", back_populates="data")


class DimPedidoCompra(Base):
    __tablename__ = "dim_pedido_compra"
    __table_args__ = {"schema": "dw_projeto"}

    id_pedido = Column(Integer, primary_key=True, index=True)
    numero_pedido = Column(String(20), unique=True, nullable=False)
    solicitacao_id = Column(Integer, nullable=True)
    fornecedor_id = Column(
        Integer,
        ForeignKey("dw_projeto.dim_fornecedor.id_fornecedor"),
        nullable=True,
    )
    data_pedido = Column(Date, nullable=True)
    data_previsao_entrega = Column(Date, nullable=True)
    valor_total = Column(Numeric(12, 2), nullable=True)
    status = Column(String(20), nullable=True)

    fornecedor = relationship("DimFornecedor", back_populates="pedidos_compra")
    compras = relationship("FactCompras", back_populates="pedido")


class FactHorasTrabalhadas(Base):
    __tablename__ = "fato_horas_trabalhadas"
    __table_args__ = {"schema": "dw_projeto"}

    id_fato_horas = Column(Integer, primary_key=True, index=True)
    programa_id = Column(
        Integer,
        ForeignKey("dw_projeto.dim_programa.id_programa"),
        nullable=True,
    )
    projeto_id = Column(
        Integer,
        ForeignKey("dw_projeto.dim_projeto.id_projeto"),
        nullable=True,
    )
    tarefa_id = Column(
        Integer,
        ForeignKey("dw_projeto.dim_tarefa.id_tarefa"),
        nullable=True,
    )
    usuario_id = Column(
        Integer,
        ForeignKey("dw_projeto.dim_usuario.id_usuario"),
        nullable=True,
    )
    data_id = Column(
        Integer,
        ForeignKey("dw_projeto.dim_data.id_data"),
        nullable=True,
    )
    horas_trabalhadas = Column(Numeric(6, 2), nullable=True)

    programa = relationship("DimPrograma", back_populates="horas_trabalhadas")
    projeto = relationship("DimProjeto", back_populates="horas_trabalhadas")
    tarefa = relationship("DimTarefa", back_populates="horas_trabalhadas")
    usuario = relationship("DimUsuario", back_populates="horas_trabalhadas")
    data = relationship("DimData", back_populates="horas_trabalhadas")


class FactConsumoMateriais(Base):
    __tablename__ = "fato_consumo_materiais"
    __table_args__ = {"schema": "dw_projeto"}

    id_fato_material = Column(Integer, primary_key=True, index=True)
    programa_id = Column(
        Integer,
        ForeignKey("dw_projeto.dim_programa.id_programa"),
        nullable=True,
    )
    projeto_id = Column(
        Integer,
        ForeignKey("dw_projeto.dim_projeto.id_projeto"),
        nullable=True,
    )
    material_id = Column(
        Integer,
        ForeignKey("dw_projeto.dim_material.id_material"),
        nullable=True,
    )
    fornecedor_id = Column(
        Integer,
        ForeignKey("dw_projeto.dim_fornecedor.id_fornecedor"),
        nullable=True,
    )
    data_id = Column(
        Integer,
        ForeignKey("dw_projeto.dim_data.id_data"),
        nullable=True,
    )
    quantidade_empenhada = Column(Integer, nullable=True)
    custo_unitario = Column(Numeric(10, 2), nullable=True)
    custo_total = Column(Numeric(12, 2), nullable=True)

    programa = relationship("DimPrograma", back_populates="consumo_materiais")
    projeto = relationship("DimProjeto", back_populates="consumo_materiais")
    material = relationship("DimMaterial", back_populates="consumo_materiais")
    fornecedor = relationship("DimFornecedor", back_populates="consumo_materiais")
    data = relationship("DimData", back_populates="consumo_materiais")


class FactCompras(Base):
    __tablename__ = "fato_compras"
    __table_args__ = {"schema": "dw_projeto"}

    id_fato_compra = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(
        Integer,
        ForeignKey("dw_projeto.dim_pedido_compra.id_pedido"),
        nullable=True,
    )
    programa_id = Column(
        Integer,
        ForeignKey("dw_projeto.dim_programa.id_programa"),
        nullable=True,
    )
    projeto_id = Column(
        Integer,
        ForeignKey("dw_projeto.dim_projeto.id_projeto"),
        nullable=True,
    )
    fornecedor_id = Column(
        Integer,
        ForeignKey("dw_projeto.dim_fornecedor.id_fornecedor"),
        nullable=True,
    )
    data_id = Column(
        Integer,
        ForeignKey("dw_projeto.dim_data.id_data"),
        nullable=True,
    )
    valor_alocado = Column(Numeric(12, 2), nullable=True)

    pedido = relationship("DimPedidoCompra", back_populates="compras")
    programa = relationship("DimPrograma", back_populates="compras")
    projeto = relationship("DimProjeto", back_populates="compras")
    fornecedor = relationship("DimFornecedor", back_populates="compras")
    data = relationship("DimData", back_populates="compras")
