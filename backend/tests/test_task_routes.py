import os
os.environ["DATABASE_URL"] = "postgresql://taskuser:taskpass@localhost:5432/taskdb_test"
os.environ["REDIS_URL"] = "redis://localhost:6379/1"
os.environ["SECRET_KEY"] = "test-secret-key-32-chars-minimum!!"

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine

@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)

def _auth_headers():
    resp = client.post("/api/auth/register", json={"email": "u@test.com", "password": "pass1234"})
    token = resp.json()["token"]
    return {"Authorization": f"Bearer {token}"}

def test_list_tasks_empty():
    resp = client.get("/api/tasks", headers=_auth_headers())
    assert resp.status_code == 200
    assert resp.json() == []

def test_create_task():
    resp = client.post("/api/tasks", json={"title": "Buy milk"}, headers=_auth_headers())
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "Buy milk"
    assert data["done"] is False
    assert "id" in data

def test_update_task_done():
    h = _auth_headers()
    task_id = client.post("/api/tasks", json={"title": "Task"}, headers=h).json()["id"]
    resp = client.patch(f"/api/tasks/{task_id}", json={"done": True}, headers=h)
    assert resp.status_code == 200
    assert resp.json()["done"] is True

def test_delete_task():
    h = _auth_headers()
    task_id = client.post("/api/tasks", json={"title": "Task"}, headers=h).json()["id"]
    resp = client.delete(f"/api/tasks/{task_id}", headers=h)
    assert resp.status_code == 204
    resp = client.get("/api/tasks", headers=h)
    assert resp.json() == []

def test_unauthenticated_returns_401():
    resp = client.get("/api/tasks")
    assert resp.status_code == 401
