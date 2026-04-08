CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS dw;

CREATE TABLE IF NOT EXISTS dw.dim_programa (
    programa_key SERIAL PRIMARY KEY,
    programa_orig_id INTEGER,
    codigo_programa VARCHAR(255),
    nome_programa VARCHAR(255),
    gerente_programa VARCHAR(255),
    gerente_tecnico VARCHAR(255),
    data_inicio DATE,
    data_fim_prevista DATE,
    status VARCHAR(255)
);

CREATE UNIQUE INDEX IF NOT EXISTS uq_dim_programa_codigo_programa
    ON dw.dim_programa (codigo_programa);

CREATE TABLE IF NOT EXISTS dw.dim_projeto (
    projeto_key SERIAL PRIMARY KEY,
    projeto_orig_id INTEGER,
    programa_key INTEGER,
    codigo_projeto VARCHAR(255),
    nome_projeto VARCHAR(255),
    responsavel VARCHAR(255),
    custo_hora NUMERIC,
    data_inicio DATE,
    data_fim_prevista DATE,
    status VARCHAR(255)
);

CREATE UNIQUE INDEX IF NOT EXISTS uq_dim_projeto_codigo_projeto
    ON dw.dim_projeto (codigo_projeto);

CREATE TABLE IF NOT EXISTS dw.dim_tarefa (
    tarefa_key SERIAL PRIMARY KEY,
    tarefa_orig_id INTEGER,
    projeto_key INTEGER,
    codigo_tarefa VARCHAR(255),
    titulo VARCHAR(255),
    responsavel VARCHAR(255),
    estimativa_horas NUMERIC,
    data_inicio DATE,
    data_fim_prevista DATE,
    status VARCHAR(255)
);

CREATE UNIQUE INDEX IF NOT EXISTS uq_dim_tarefa_codigo_tarefa
    ON dw.dim_tarefa (codigo_tarefa);

CREATE TABLE IF NOT EXISTS dw.dim_material (
    material_key SERIAL PRIMARY KEY,
    material_orig_id INTEGER,
    codigo_material VARCHAR(255),
    descricao VARCHAR(255),
    categoria VARCHAR(255),
    fabricante VARCHAR(255),
    custo_estimado NUMERIC,
    status VARCHAR(255)
);

CREATE UNIQUE INDEX IF NOT EXISTS uq_dim_material_codigo_material
    ON dw.dim_material (codigo_material);

CREATE TABLE IF NOT EXISTS dw.dim_fornecedor (
    fornecedor_key SERIAL PRIMARY KEY,
    fornecedor_orig_id INTEGER,
    codigo_fornecedor VARCHAR(255),
    razao_social VARCHAR(255),
    cidade VARCHAR(255),
    estado VARCHAR(255),
    categoria VARCHAR(255),
    status VARCHAR(255)
);

CREATE UNIQUE INDEX IF NOT EXISTS uq_dim_fornecedor_codigo_fornecedor
    ON dw.dim_fornecedor (codigo_fornecedor);

CREATE TABLE IF NOT EXISTS dw.dim_usuario (
    usuario_key SERIAL PRIMARY KEY,
    nome_usuario VARCHAR(255)
);

CREATE UNIQUE INDEX IF NOT EXISTS uq_dim_usuario_nome_usuario
    ON dw.dim_usuario (nome_usuario);

CREATE TABLE IF NOT EXISTS dw.dim_localizacao (
    localizacao_key SERIAL PRIMARY KEY,
    localizacao VARCHAR(255)
);

CREATE UNIQUE INDEX IF NOT EXISTS uq_dim_localizacao_localizacao
    ON dw.dim_localizacao (localizacao);

CREATE TABLE IF NOT EXISTS dw.dim_data (
    data_key SERIAL PRIMARY KEY,
    data DATE,
    ano INTEGER,
    mes INTEGER,
    dia INTEGER,
    trimestre INTEGER,
    nome_mes VARCHAR(255),
    dia_semana INTEGER
);

CREATE UNIQUE INDEX IF NOT EXISTS uq_dim_data_data
    ON dw.dim_data (data);


CREATE TABLE IF NOT EXISTS dw.fato_horas_trabalhadas (
    fato_horas_key SERIAL PRIMARY KEY,
    horas_trabalhadas_orig_id INTEGER,
    tarefa_key INTEGER,
    usuario_key INTEGER,
    data_key INTEGER,
    horas_trabalhadas NUMERIC
);

CREATE UNIQUE INDEX IF NOT EXISTS uq_fato_horas_trabalhadas_orig_id
    ON dw.fato_horas_trabalhadas (horas_trabalhadas_orig_id);

CREATE TABLE IF NOT EXISTS dw.fato_solicitacoes_compra (
    fato_solicitacao_key SERIAL PRIMARY KEY,
    solicitacao_orig_id INTEGER,
    numero_solicitacao VARCHAR(255),
    projeto_key INTEGER,
    material_key INTEGER,
    data_key INTEGER,
    quantidade NUMERIC,
    prioridade VARCHAR(255),
    status VARCHAR(255)
);

CREATE UNIQUE INDEX IF NOT EXISTS uq_fato_solicitacoes_compra_orig_id
    ON dw.fato_solicitacoes_compra (solicitacao_orig_id);

CREATE TABLE IF NOT EXISTS dw.fato_pedidos_compra (
    fato_pedido_key SERIAL PRIMARY KEY,
    pedido_compra_orig_id INTEGER,
    numero_pedido VARCHAR(255),
    solicitacao_id INTEGER,
    projeto_id INTEGER,
    material_id INTEGER,
    fornecedor_key INTEGER,
    data_pedido_key INTEGER,
    data_previsao_key INTEGER,
    valor_total NUMERIC,
    status VARCHAR(255)
);

CREATE UNIQUE INDEX IF NOT EXISTS uq_fato_pedidos_compra_orig_id
    ON dw.fato_pedidos_compra (pedido_compra_orig_id);

CREATE TABLE IF NOT EXISTS dw.fato_compras_projeto (
    fato_compra_projeto_key SERIAL PRIMARY KEY,
    compra_projeto_orig_id INTEGER,
    pedido_compra_id INTEGER,
    projeto_key INTEGER,
    valor_alocado NUMERIC
);

CREATE UNIQUE INDEX IF NOT EXISTS uq_fato_compras_projeto_orig_id
    ON dw.fato_compras_projeto (compra_projeto_orig_id);

CREATE TABLE IF NOT EXISTS dw.fato_empenho_materiais (
    fato_empenho_key SERIAL PRIMARY KEY,
    empenho_material_orig_id INTEGER,
    projeto_key INTEGER,
    material_key INTEGER,
    data_key INTEGER,
    quantidade_empenhada NUMERIC
);

CREATE UNIQUE INDEX IF NOT EXISTS uq_fato_empenho_materiais_orig_id
    ON dw.fato_empenho_materiais (empenho_material_orig_id);

CREATE TABLE IF NOT EXISTS dw.fato_estoque_materiais_projeto (
    fato_estoque_key SERIAL PRIMARY KEY,
    estoque_material_projeto_orig_id INTEGER,
    projeto_key INTEGER,
    material_key INTEGER,
    localizacao_key INTEGER,
    quantidade NUMERIC
);

CREATE UNIQUE INDEX IF NOT EXISTS uq_fato_estoque_materiais_projeto_orig_id
    ON dw.fato_estoque_materiais_projeto (estoque_material_projeto_orig_id);

ALTER TABLE dw.dim_projeto
    DROP CONSTRAINT IF EXISTS fk_dim_projeto_programa_key;
ALTER TABLE dw.dim_projeto
    ADD CONSTRAINT fk_dim_projeto_programa_key
    FOREIGN KEY (programa_key) REFERENCES dw.dim_programa(programa_key);

ALTER TABLE dw.dim_tarefa
    DROP CONSTRAINT IF EXISTS fk_dim_tarefa_projeto_key;
ALTER TABLE dw.dim_tarefa
    ADD CONSTRAINT fk_dim_tarefa_projeto_key
    FOREIGN KEY (projeto_key) REFERENCES dw.dim_projeto(projeto_key);

ALTER TABLE dw.fato_horas_trabalhadas
    DROP CONSTRAINT IF EXISTS fk_fato_horas_tarefa_key;
ALTER TABLE dw.fato_horas_trabalhadas
    ADD CONSTRAINT fk_fato_horas_tarefa_key
    FOREIGN KEY (tarefa_key) REFERENCES dw.dim_tarefa(tarefa_key);

ALTER TABLE dw.fato_horas_trabalhadas
    DROP CONSTRAINT IF EXISTS fk_fato_horas_usuario_key;
ALTER TABLE dw.fato_horas_trabalhadas
    ADD CONSTRAINT fk_fato_horas_usuario_key
    FOREIGN KEY (usuario_key) REFERENCES dw.dim_usuario(usuario_key);

ALTER TABLE dw.fato_horas_trabalhadas
    DROP CONSTRAINT IF EXISTS fk_fato_horas_data_key;
ALTER TABLE dw.fato_horas_trabalhadas
    ADD CONSTRAINT fk_fato_horas_data_key
    FOREIGN KEY (data_key) REFERENCES dw.dim_data(data_key);

ALTER TABLE dw.fato_solicitacoes_compra
    DROP CONSTRAINT IF EXISTS fk_fato_solicitacoes_projeto_key;
ALTER TABLE dw.fato_solicitacoes_compra
    ADD CONSTRAINT fk_fato_solicitacoes_projeto_key
    FOREIGN KEY (projeto_key) REFERENCES dw.dim_projeto(projeto_key);

ALTER TABLE dw.fato_solicitacoes_compra
    DROP CONSTRAINT IF EXISTS fk_fato_solicitacoes_material_key;
ALTER TABLE dw.fato_solicitacoes_compra
    ADD CONSTRAINT fk_fato_solicitacoes_material_key
    FOREIGN KEY (material_key) REFERENCES dw.dim_material(material_key);

ALTER TABLE dw.fato_solicitacoes_compra
    DROP CONSTRAINT IF EXISTS fk_fato_solicitacoes_data_key;
ALTER TABLE dw.fato_solicitacoes_compra
    ADD CONSTRAINT fk_fato_solicitacoes_data_key
    FOREIGN KEY (data_key) REFERENCES dw.dim_data(data_key);

ALTER TABLE dw.fato_pedidos_compra
    DROP CONSTRAINT IF EXISTS fk_fato_pedidos_fornecedor_key;
ALTER TABLE dw.fato_pedidos_compra
    ADD CONSTRAINT fk_fato_pedidos_fornecedor_key
    FOREIGN KEY (fornecedor_key) REFERENCES dw.dim_fornecedor(fornecedor_key);

ALTER TABLE dw.fato_pedidos_compra
    DROP CONSTRAINT IF EXISTS fk_fato_pedidos_data_pedido_key;
ALTER TABLE dw.fato_pedidos_compra
    ADD CONSTRAINT fk_fato_pedidos_data_pedido_key
    FOREIGN KEY (data_pedido_key) REFERENCES dw.dim_data(data_key);

ALTER TABLE dw.fato_pedidos_compra
    DROP CONSTRAINT IF EXISTS fk_fato_pedidos_data_previsao_key;
ALTER TABLE dw.fato_pedidos_compra
    ADD CONSTRAINT fk_fato_pedidos_data_previsao_key
    FOREIGN KEY (data_previsao_key) REFERENCES dw.dim_data(data_key);

ALTER TABLE dw.fato_compras_projeto
    DROP CONSTRAINT IF EXISTS fk_fato_compras_projeto_projeto_key;
ALTER TABLE dw.fato_compras_projeto
    ADD CONSTRAINT fk_fato_compras_projeto_projeto_key
    FOREIGN KEY (projeto_key) REFERENCES dw.dim_projeto(projeto_key);

ALTER TABLE dw.fato_empenho_materiais
    DROP CONSTRAINT IF EXISTS fk_fato_empenho_projeto_key;
ALTER TABLE dw.fato_empenho_materiais
    ADD CONSTRAINT fk_fato_empenho_projeto_key
    FOREIGN KEY (projeto_key) REFERENCES dw.dim_projeto(projeto_key);

ALTER TABLE dw.fato_empenho_materiais
    DROP CONSTRAINT IF EXISTS fk_fato_empenho_material_key;
ALTER TABLE dw.fato_empenho_materiais
    ADD CONSTRAINT fk_fato_empenho_material_key
    FOREIGN KEY (material_key) REFERENCES dw.dim_material(material_key);

ALTER TABLE dw.fato_empenho_materiais
    DROP CONSTRAINT IF EXISTS fk_fato_empenho_data_key;
ALTER TABLE dw.fato_empenho_materiais
    ADD CONSTRAINT fk_fato_empenho_data_key
    FOREIGN KEY (data_key) REFERENCES dw.dim_data(data_key);

ALTER TABLE dw.fato_estoque_materiais_projeto
    DROP CONSTRAINT IF EXISTS fk_fato_estoque_projeto_key;
ALTER TABLE dw.fato_estoque_materiais_projeto
    ADD CONSTRAINT fk_fato_estoque_projeto_key
    FOREIGN KEY (projeto_key) REFERENCES dw.dim_projeto(projeto_key);

ALTER TABLE dw.fato_estoque_materiais_projeto
    DROP CONSTRAINT IF EXISTS fk_fato_estoque_material_key;
ALTER TABLE dw.fato_estoque_materiais_projeto
    ADD CONSTRAINT fk_fato_estoque_material_key
    FOREIGN KEY (material_key) REFERENCES dw.dim_material(material_key);

ALTER TABLE dw.fato_estoque_materiais_projeto
    DROP CONSTRAINT IF EXISTS fk_fato_estoque_localizacao_key;
ALTER TABLE dw.fato_estoque_materiais_projeto
    ADD CONSTRAINT fk_fato_estoque_localizacao_key
    FOREIGN KEY (localizacao_key) REFERENCES dw.dim_localizacao(localizacao_key);