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

def test_register_success():
    resp = client.post("/api/auth/register", json={"email": "a@b.com", "password": "secret123"})
    assert resp.status_code == 201
    assert "token" in resp.json()

def test_register_duplicate_email():
    client.post("/api/auth/register", json={"email": "a@b.com", "password": "secret123"})
    resp = client.post("/api/auth/register", json={"email": "a@b.com", "password": "other"})
    assert resp.status_code == 400

def test_login_success():
    client.post("/api/auth/register", json={"email": "a@b.com", "password": "secret123"})
    resp = client.post("/api/auth/login", json={"email": "a@b.com", "password": "secret123"})
    assert resp.status_code == 200
    assert "token" in resp.json()

def test_login_wrong_password():
    client.post("/api/auth/register", json={"email": "a@b.com", "password": "secret123"})
    resp = client.post("/api/auth/login", json={"email": "a@b.com", "password": "wrong"})
    assert resp.status_code == 401
