import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.db.database import get_db


class FakeExecuteResult:
    def __init__(self, value):
        self.value = value

    def fetchone(self):
        return (self.value,)


class FakeQuery:
    def __init__(self, data):
        self._data = data

    def all(self):
        return self._data


class FakeSession:
    def __init__(self, query_data=None, execute_result=1, execute_error=None):
        self.query_data = query_data or {}
        self.execute_result = execute_result
        self.execute_error = execute_error

    def execute(self, sql):
        if self.execute_error:
            raise self.execute_error
        return FakeExecuteResult(self.execute_result)

    def query(self, model):
        return FakeQuery(self.query_data.get(model, []))


@pytest.fixture
def client():
    # garante que cada teste comece limpo
    app.dependency_overrides = {}
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides = {}


@pytest.fixture
def override_db():
    def _override(fake_db):
        def get_test_db():
            yield fake_db
        app.dependency_overrides[get_db] = get_test_db

    return _override