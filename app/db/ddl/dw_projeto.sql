CREATE SCHEMA dw_projeto;
SET search_path TO dw_projeto;

CREATE TABLE dw_projeto.dim_programa (
    id_programa SERIAL PRIMARY KEY,
    codigo_programa VARCHAR(20) UNIQUE,
    nome_programa VARCHAR(200),
    gerente_programa VARCHAR(100),
    gerente_tecnico VARCHAR(100),
    data_inicio DATE,
    data_fim_prevista DATE,
    status VARCHAR(20)
);

CREATE TABLE dw_projeto.dim_projeto (
    id_projeto SERIAL PRIMARY KEY,
    codigo_projeto VARCHAR(20) UNIQUE,
    nome_projeto VARCHAR(200),
    programa_id INT,
    responsavel VARCHAR(100),
    custo_hora NUMERIC(10,2),
    data_inicio DATE,
    data_fim_prevista DATE,
    status VARCHAR(20),
    CONSTRAINT fk_dim_projeto_programa
        FOREIGN KEY (programa_id)
        REFERENCES dw_projeto.dim_programa(id_programa)
);

CREATE TABLE dw_projeto.dim_material (
    id_material SERIAL PRIMARY KEY,
    codigo_material VARCHAR(50) UNIQUE,
    descricao TEXT,
    categoria VARCHAR(100),
    fabricante VARCHAR(100),
    custo_estimado NUMERIC(10,2),
    status VARCHAR(20)
);

CREATE TABLE dw_projeto.dim_fornecedor (
    id_fornecedor SERIAL PRIMARY KEY,
    codigo_fornecedor VARCHAR(20) UNIQUE,
    razao_social VARCHAR(200),
    cidade VARCHAR(100),
    estado VARCHAR(50),
    categoria VARCHAR(100),
    status VARCHAR(20)
);

CREATE TABLE dw_projeto.dim_usuario (
    id_usuario SERIAL PRIMARY KEY,
    nome_usuario VARCHAR(100) UNIQUE
);

CREATE TABLE dw_projeto.dim_tarefa (
    id_tarefa SERIAL PRIMARY KEY,
    codigo_tarefa VARCHAR(20) UNIQUE,
    projeto_id INT,
    titulo VARCHAR(200),
    responsavel VARCHAR(100),
    estimativa_horas INT,
    data_inicio DATE,
    data_fim_prevista DATE,
    status VARCHAR(20),
    CONSTRAINT fk_dim_tarefa_projeto
        FOREIGN KEY (projeto_id)
        REFERENCES dw_projeto.dim_projeto(id_projeto)
);

CREATE TABLE dw_projeto.dim_data (
    id_data SERIAL PRIMARY KEY,
    data DATE UNIQUE,
    dia INT,
    mes INT,
    nome_mes VARCHAR(20),
    trimestre INT,
    ano INT,
    dia_semana INT,
    nome_dia_semana VARCHAR(20)
);

CREATE TABLE dw_projeto.dim_pedido_compra (
    id_pedido SERIAL PRIMARY KEY,
    numero_pedido VARCHAR(20) UNIQUE,
    solicitacao_id INT,
    fornecedor_id INT,
    data_pedido DATE,
    data_previsao_entrega DATE,
    valor_total NUMERIC(12,2),
    status VARCHAR(20),
    CONSTRAINT fk_dim_pedido_fornecedor
        FOREIGN KEY (fornecedor_id)
        REFERENCES dw_projeto.dim_fornecedor(id_fornecedor)
);

CREATE TABLE dw_projeto.fato_horas_trabalhadas (
    id_fato_horas SERIAL PRIMARY KEY,
    programa_id INT,
    projeto_id INT,
    tarefa_id INT,
    usuario_id INT,
    data_id INT,
    horas_trabalhadas NUMERIC(6,2),
    CONSTRAINT fk_fht_programa
        FOREIGN KEY (programa_id)
        REFERENCES dw_projeto.dim_programa(id_programa),
    CONSTRAINT fk_fht_projeto
        FOREIGN KEY (projeto_id)
        REFERENCES dw_projeto.dim_projeto(id_projeto),
    CONSTRAINT fk_fht_tarefa
        FOREIGN KEY (tarefa_id)
        REFERENCES dw_projeto.dim_tarefa(id_tarefa),
    CONSTRAINT fk_fht_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES dw_projeto.dim_usuario(id_usuario),
    CONSTRAINT fk_fht_data
        FOREIGN KEY (data_id)
        REFERENCES dw_projeto.dim_data(id_data)
);

CREATE TABLE dw_projeto.fato_consumo_materiais (
    id_fato_material SERIAL PRIMARY KEY,
    programa_id INT,
    projeto_id INT,
    material_id INT,
    fornecedor_id INT,
    data_id INT,
    quantidade_empenhada INT,
    custo_unitario NUMERIC(10,2),
    custo_total NUMERIC(12,2),
    CONSTRAINT fk_fcm_programa
        FOREIGN KEY (programa_id)
        REFERENCES dw_projeto.dim_programa(id_programa),
    CONSTRAINT fk_fcm_projeto
        FOREIGN KEY (projeto_id)
        REFERENCES dw_projeto.dim_projeto(id_projeto),
    CONSTRAINT fk_fcm_material
        FOREIGN KEY (material_id)
        REFERENCES dw_projeto.dim_material(id_material),
    CONSTRAINT fk_fcm_fornecedor
        FOREIGN KEY (fornecedor_id)
        REFERENCES dw_projeto.dim_fornecedor(id_fornecedor),
    CONSTRAINT fk_fcm_data
        FOREIGN KEY (data_id)
        REFERENCES dw_projeto.dim_data(id_data)
);

CREATE TABLE dw_projeto.fato_compras (
    id_fato_compra SERIAL PRIMARY KEY,
    pedido_id INT,
    programa_id INT,
    projeto_id INT,
    fornecedor_id INT,
    data_id INT,
    valor_alocado NUMERIC(12,2),
    CONSTRAINT fk_fc_pedido
        FOREIGN KEY (pedido_id)
        REFERENCES dw_projeto.dim_pedido_compra(id_pedido),
    CONSTRAINT fk_fc_programa
        FOREIGN KEY (programa_id)
        REFERENCES dw_projeto.dim_programa(id_programa),
    CONSTRAINT fk_fc_projeto
        FOREIGN KEY (projeto_id)
        REFERENCES dw_projeto.dim_projeto(id_projeto),
    CONSTRAINT fk_fc_fornecedor
        FOREIGN KEY (fornecedor_id)
        REFERENCES dw_projeto.dim_fornecedor(id_fornecedor),
    CONSTRAINT fk_fc_data
        FOREIGN KEY (data_id)
        REFERENCES dw_projeto.dim_data(id_data)
);