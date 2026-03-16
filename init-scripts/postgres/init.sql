CREATE SCHEMA dw_projeto;
SET search_path TO dw_projeto;

CREATE TABLE dim_programa (
    id_programa SERIAL PRIMARY KEY,
    codigo_programa VARCHAR(20),
    nome_programa VARCHAR(200),
    gerente_programa VARCHAR(100),
    status VARCHAR(20)
);

CREATE TABLE dim_projeto (
    id_projeto SERIAL PRIMARY KEY,
    codigo_projeto VARCHAR(20),
    nome_projeto VARCHAR(200),
    responsavel VARCHAR(100),
    data_inicio DATE,
    status VARCHAR(20)
);

CREATE TABLE dim_material (
    id_material SERIAL PRIMARY KEY,
    codigo_material VARCHAR(50),
    categoria VARCHAR(100),
    descricao TEXT,
    fabricante VARCHAR(100),
    unidade_medida VARCHAR(20),
    lead_time_dias INT,
    custo_estimado NUMERIC(10,2)
);

CREATE TABLE dim_fornecedor (
    id_fornecedor SERIAL PRIMARY KEY,
    razao_social VARCHAR(200),
    nome_fantasia VARCHAR(200),
    cidade VARCHAR(100),
    estado VARCHAR(50),
    email VARCHAR(100),
    telefone VARCHAR(30),
    categoria_fornecedor VARCHAR(50),
	cnpj VARCHAR(20),
	condicao_pagamento VARCHAR(20),
    status VARCHAR(20),
	data_cadastro DATE
);

CREATE TABLE dim_usuario (
    id_usuario SERIAL PRIMARY KEY,
    nome_usuario VARCHAR(100),
    departamento VARCHAR(100)
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
    trimestre INT,
    ano INT
);

CREATE TABLE fact_consumo_materiais (
    id_fato_material SERIAL PRIMARY KEY,

    programa_id INT,
    projeto_id INT,
    material_id INT,
    fornecedor_id INT,
    data_id INT,

    quantidade_empenhada INT,
    custo_unitario NUMERIC(10,2),
    custo_total NUMERIC(12,2),

    CONSTRAINT fk_programa_material FOREIGN KEY (programa_id) REFERENCES dim_programa(id_programa),
    CONSTRAINT fk_projeto_material FOREIGN KEY (projeto_id) REFERENCES dim_projeto(id_projeto),
    CONSTRAINT fk_material FOREIGN KEY (material_id) REFERENCES dim_material(id_material),
    CONSTRAINT fk_fornecedor FOREIGN KEY (fornecedor_id) REFERENCES dim_fornecedor(id_fornecedor),
    CONSTRAINT fk_data_material FOREIGN KEY (data_id) REFERENCES dim_data(id_data)
);

CREATE TABLE fact_horas_trabalhadas (
    id_fato_horas SERIAL PRIMARY KEY,

    programa_id INT,
    projeto_id INT,
    tarefa_id INT,
    usuario_id INT,
    data_id INT,

    horas_trabalhadas NUMERIC(6,2),
    custo_hora NUMERIC(10,2),
    custo_total_hora NUMERIC(12,2),

    CONSTRAINT fk_programa_horas FOREIGN KEY (programa_id) REFERENCES dim_programa(id_programa),
    CONSTRAINT fk_projeto_horas FOREIGN KEY (projeto_id) REFERENCES dim_projeto(id_projeto),
    CONSTRAINT fk_tarefa FOREIGN KEY (tarefa_id) REFERENCES dim_tarefa(id_tarefa),
    CONSTRAINT fk_usuario FOREIGN KEY (usuario_id) REFERENCES dim_usuario(id_usuario),
    CONSTRAINT fk_data_horas FOREIGN KEY (data_id) REFERENCES dim_data(id_data)
);