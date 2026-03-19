CREATE SCHEMA dw_projeto;
SET search_path TO dw_projeto;

CREATE TABLE dim_programa (
    id_programa SERIAL PRIMARY KEY,
    codigo_programa VARCHAR(20),
    nome_programa VARCHAR(200),
    gerente_programa VARCHAR(100),
    gerente_tecnico VARCHAR(100),
    data_inicio DATE,
    data_fim_prevista DATE,
    status VARCHAR(20)
);

CREATE TABLE dim_projeto (
    id_projeto SERIAL PRIMARY KEY,
    codigo_projeto VARCHAR(20),
    nome_projeto VARCHAR(200),
    programa_id INT,
    responsavel VARCHAR(100),
    custo_hora NUMERIC(10,2),
    data_inicio DATE,
    data_fim_prevista DATE,
    status VARCHAR(20),
    FOREIGN KEY (programa_id) REFERENCES dim_programa(id_programa)
);

CREATE TABLE dim_material (
    id_material SERIAL PRIMARY KEY,
    codigo_material VARCHAR(50),
    descricao TEXT,
    categoria VARCHAR(100),
    fabricante VARCHAR(100),
    custo_estimado NUMERIC(10,2),
    status VARCHAR(20)
);

CREATE TABLE dim_fornecedor (
    id_fornecedor SERIAL PRIMARY KEY,
    codigo_fornecedor VARCHAR(20),
    razao_social VARCHAR(200),
    cidade VARCHAR(100),
    estado VARCHAR(50),
    categoria VARCHAR(100),
    status VARCHAR(20)
);

CREATE TABLE dim_usuario (
    id_usuario SERIAL PRIMARY KEY,
    nome_usuario VARCHAR(100)
);

CREATE TABLE dim_tarefa (
    id_tarefa SERIAL PRIMARY KEY,
    codigo_tarefa VARCHAR(20),
    titulo VARCHAR(200),
    estimativa_horas INT,
    status VARCHAR(20)
);

CREATE TABLE dim_data (
    id_data SERIAL PRIMARY KEY,
    data DATE,
    dia INT,
    mes INT,
    nome_mes VARCHAR(20),
    trimestre INT,
    ano INT,
    dia_semana INT,
    nome_dia_semana VARCHAR(20)
);

CREATE TABLE fato_horas_trabalhadas (
    id_fato_horas SERIAL PRIMARY KEY,
    programa_id INT,
    projeto_id INT,
    tarefa_id INT,
    usuario_id INT,
    data_id INT,
    horas_trabalhadas NUMERIC(6,2),
    FOREIGN KEY (programa_id) REFERENCES dim_programa(id_programa),
    FOREIGN KEY (projeto_id) REFERENCES dim_projeto(id_projeto),
    FOREIGN KEY (tarefa_id) REFERENCES dim_tarefa(id_tarefa),
    FOREIGN KEY (usuario_id) REFERENCES dim_usuario(id_usuario),
    FOREIGN KEY (data_id) REFERENCES dim_data(id_data)
);

CREATE TABLE fato_consumo_materiais (
    id_fato_material SERIAL PRIMARY KEY,
    programa_id INT,
    projeto_id INT,
    material_id INT,
    fornecedor_id INT,
    data_id INT,
    quantidade_empenhada INT,
    custo_unitario NUMERIC(10,2),
    custo_total NUMERIC(12,2),
    FOREIGN KEY (programa_id) REFERENCES dim_programa(id_programa),
    FOREIGN KEY (projeto_id) REFERENCES dim_projeto(id_projeto),
    FOREIGN KEY (material_id) REFERENCES dim_material(id_material),
    FOREIGN KEY (fornecedor_id) REFERENCES dim_fornecedor(id_fornecedor),
    FOREIGN KEY (data_id) REFERENCES dim_data(id_data)
);