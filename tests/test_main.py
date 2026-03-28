from tests.conftest import FakeSession


def test_root_endpoint(client):
    response = client.get("/")

    assert response.status_code == 200
    body = response.json()

    assert body["message"] == "API Python para Data Warehouse Projeto"
    assert body["status"] == "online"
    assert "version" in body


def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_db_test_success(client, override_db):
    fake_db = FakeSession(execute_result=1)
    override_db(fake_db)

    response = client.get("/db-test")

    assert response.status_code == 200
    assert response.json() == {
        "status": "Database connected",
        "result": 1
    }


def test_db_test_failure(client, override_db):
    fake_db = FakeSession(execute_error=Exception("erro de conexão"))
    override_db(fake_db)

    response = client.get("/db-test")

    assert response.status_code == 200
    body = response.json()

    assert body["status"] == "Database connection failed"
    assert body["error"] == "erro de conexão"