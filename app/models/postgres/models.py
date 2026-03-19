from sqlalchemy import Column, Integer, String, Date, Numeric, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class DimPrograma(Base):
    __tablename__ = "dim_programa"
    __table_args__ = {"schema": "dw_projeto"}

    id_programa = Column(Integer, primary_key=True, index=True)
    codigo_programa = Column(String(20))
    nome_programa = Column(String(200))
    gerente_programa = Column(String(100))
    gerente_tecnico = Column(String(100))
    data_inicio = Column(Date)
    data_fim_prevista = Column(Date)
    status = Column(String(20))

class DimProjeto(Base):
    __tablename__ = "dim_projeto"
    __table_args__ = {"schema": "dw_projeto"}

    id_projeto = Column(Integer, primary_key=True, index=True)
    codigo_projeto = Column(String(20))
    nome_projeto = Column(String(200))
    programa_id = Column(Integer, ForeignKey("dw_projeto.dim_programa.id_programa"))
    responsavel = Column(String(100))
    custo_hora = Column(Numeric(10, 2))
    data_inicio = Column(Date)
    data_fim_prevista = Column(Date)
    status = Column(String(20))

    programa = relationship("DimPrograma")

class DimMaterial(Base):
    __tablename__ = "dim_material"
    __table_args__ = {"schema": "dw_projeto"}

    id_material = Column(Integer, primary_key=True, index=True)
    codigo_material = Column(String(50))
    descricao = Column(Text)
    categoria = Column(String(100))
    fabricante = Column(String(100))
    custo_estimado = Column(Numeric(10, 2))
    status = Column(String(20))

class DimFornecedor(Base):
    __tablename__ = "dim_fornecedor"
    __table_args__ = {"schema": "dw_projeto"}

    id_fornecedor = Column(Integer, primary_key=True, index=True)
    codigo_fornecedor = Column(String(20))
    razao_social = Column(String(200))
    cidade = Column(String(100))
    estado = Column(String(50))
    categoria = Column(String(100))
    status = Column(String(20))

class DimUsuario(Base):
    __tablename__ = "dim_usuario"
    __table_args__ = {"schema": "dw_projeto"}

    id_usuario = Column(Integer, primary_key=True, index=True)
    nome_usuario = Column(String(100))

class DimTarefa(Base):
    __tablename__ = "dim_tarefa"
    __table_args__ = {"schema": "dw_projeto"}

    id_tarefa = Column(Integer, primary_key=True, index=True)
    codigo_tarefa = Column(String(20))
    titulo = Column(String(200))
    estimativa_horas = Column(Integer)
    status = Column(String(20))

class DimData(Base):
    __tablename__ = "dim_data"
    __table_args__ = {"schema": "dw_projeto"}

    id_data = Column(Integer, primary_key=True, index=True)
    data = Column(Date)
    dia = Column(Integer)
    mes = Column(Integer)
    nome_mes = Column(String(20))
    trimestre = Column(Integer)
    ano = Column(Integer)
    dia_semana = Column(Integer)
    nome_dia_semana = Column(String(20))

class FactConsumoMateriais(Base):
    __tablename__ = "fato_consumo_materiais"
    __table_args__ = {"schema": "dw_projeto"}

    id_fato_material = Column(Integer, primary_key=True, index=True)
    programa_id = Column(Integer, ForeignKey("dw_projeto.dim_programa.id_programa"))
    projeto_id = Column(Integer, ForeignKey("dw_projeto.dim_projeto.id_projeto"))
    material_id = Column(Integer, ForeignKey("dw_projeto.dim_material.id_material"))
    fornecedor_id = Column(Integer, ForeignKey("dw_projeto.dim_fornecedor.id_fornecedor"))
    data_id = Column(Integer, ForeignKey("dw_projeto.dim_data.id_data"))
    quantidade_empenhada = Column(Integer)
    custo_unitario = Column(Numeric(10, 2))
    custo_total = Column(Numeric(12, 2))

    programa = relationship("DimPrograma")
    projeto = relationship("DimProjeto")
    material = relationship("DimMaterial")
    fornecedor = relationship("DimFornecedor")
    data = relationship("DimData")

class FactHorasTrabalhadas(Base):
    __tablename__ = "fato_horas_trabalhadas"
    __table_args__ = {"schema": "dw_projeto"}

    id_fato_horas = Column(Integer, primary_key=True, index=True)
    programa_id = Column(Integer, ForeignKey("dw_projeto.dim_programa.id_programa"))
    projeto_id = Column(Integer, ForeignKey("dw_projeto.dim_projeto.id_projeto"))
    tarefa_id = Column(Integer, ForeignKey("dw_projeto.dim_tarefa.id_tarefa"))
    usuario_id = Column(Integer, ForeignKey("dw_projeto.dim_usuario.id_usuario"))
    data_id = Column(Integer, ForeignKey("dw_projeto.dim_data.id_data"))
    horas_trabalhadas = Column(Numeric(6, 2))

    programa = relationship("DimPrograma")
    projeto = relationship("DimProjeto")
    tarefa = relationship("DimTarefa")
    usuario = relationship("DimUsuario")
    data = relationship("DimData")