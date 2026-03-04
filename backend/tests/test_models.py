import os
os.environ["DATABASE_URL"] = "postgresql://taskuser:taskpass@localhost:5432/taskdb_test"
os.environ["REDIS_URL"] = "redis://localhost:6379/1"
os.environ["SECRET_KEY"] = "test-secret-key-32-chars-minimum!!"

from app.database import engine, Base
from app.models import User, Task

def test_tables_created():
    Base.metadata.create_all(bind=engine)
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    assert "users" in tables
    assert "tasks" in tables
    Base.metadata.drop_all(bind=engine)
