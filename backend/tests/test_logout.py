import os
os.environ["DATABASE_URL"] = "postgresql://taskuser:taskpass@localhost:5432/taskdb_test"
os.environ["REDIS_URL"] = "redis://localhost:6379/1"
os.environ["SECRET_KEY"] = "test-secret-key-32-chars-minimum!!"

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine
from app.redis_client import get_redis

@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.create_all(bind=engine)
    get_redis().flushdb()
    yield
    Base.metadata.drop_all(bind=engine)
    get_redis().flushdb()

client = TestClient(app)

def test_logout_blacklists_token():
    resp = client.post("/api/auth/register", json={"email": "u@x.com", "password": "pass1234"})
    token = resp.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Works before logout
    assert client.get("/api/tasks", headers=headers).status_code == 200

    # Logout
    assert client.post("/api/auth/logout", headers=headers).status_code == 200

    # Rejected after logout
    assert client.get("/api/tasks", headers=headers).status_code == 401
