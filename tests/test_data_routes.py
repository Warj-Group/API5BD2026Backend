from datetime import date
from decimal import Decimal

from tests.conftest import FakeSession
from app.models.postgres.models import (
    DimPrograma,
    DimProjeto,
    DimMaterial,
    DimFornecedor,
    DimUsuario,
    DimTarefa,
    DimData,
    FactConsumoMateriais,
    FactHorasTrabalhadas,
)


def test_get_programas(client, override_db):
    programa = DimPrograma()
    programa.id_programa = 1
    programa.codigo_programa = "PRG001"
    programa.nome_programa = "Programa Alpha"
    programa.gerente_programa = "João"
    programa.gerente_tecnico = "Maria"
    programa.data_inicio = date(2026, 1, 1)
    programa.data_fim_prevista = date(2026, 12, 31)
    programa.status = "ATIVO"

    fake_db = FakeSession(query_data={DimPrograma: [programa]})
    override_db(fake_db)

    response = client.get("/data/programas")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "codigo_programa": "PRG001",
            "nome_programa": "Programa Alpha",
            "gerente_programa": "João",
            "gerente_tecnico": "Maria",
            "data_inicio": "2026-01-01",
            "data_fim_prevista": "2026-12-31",
            "status": "ATIVO",
        }
    ]


def test_get_usuarios(client, override_db):
    usuario = DimUsuario()
    usuario.id_usuario = 10
    usuario.nome_usuario = "Aline"

    fake_db = FakeSession(query_data={DimUsuario: [usuario]})
    override_db(fake_db)

    response = client.get("/data/usuarios")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 10,
            "nome_usuario": "Aline"
        }
    ]


def test_get_tarefas(client, override_db):
    tarefa = DimTarefa()
    tarefa.id_tarefa = 5
    tarefa.codigo_tarefa = "TK-001"
    tarefa.titulo = "Implementar API"
    tarefa.estimativa_horas = 16
    tarefa.status = "EM_ANDAMENTO"

    fake_db = FakeSession(query_data={DimTarefa: [tarefa]})
    override_db(fake_db)

    response = client.get("/data/tarefas")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 5,
            "codigo": "TK-001",
            "titulo": "Implementar API",
            "estimativa_horas": 16,
            "status": "EM_ANDAMENTO",
        }
    ]


def test_get_projetos_empty_list(client, override_db):
    fake_db = FakeSession(query_data={DimProjeto: []})
    override_db(fake_db)

    response = client.get("/data/projetos")

    assert response.status_code == 200
    assert response.json() == []


def test_get_materiais(client, override_db):
    material = DimMaterial()
    material.id_material = 2
    material.codigo_material = "MAT001"
    material.descricao = "Chapa de aço"
    material.categoria = "Metal"
    material.fabricante = "Fornecedor X"
    material.custo_estimado = Decimal("125.50")
    material.status = "ATIVO"

    fake_db = FakeSession(query_data={DimMaterial: [material]})
    override_db(fake_db)

    response = client.get("/data/materiais")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 2,
            "codigo_material": "MAT001",
            "descricao": "Chapa de aço",
            "categoria": "Metal",
            "fabricante": "Fornecedor X",
            "custo_estimado": 125.5,
            "status": "ATIVO",
        }
    ]