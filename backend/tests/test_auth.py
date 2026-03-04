import os
os.environ["DATABASE_URL"] = "postgresql://taskuser:taskpass@localhost:5432/taskdb_test"
os.environ["REDIS_URL"] = "redis://localhost:6379/1"
os.environ["SECRET_KEY"] = "test-secret-key-32-chars-minimum!!"

from app.auth import hash_password, verify_password, create_token, decode_token

def test_password_hash_and_verify():
    pw = "mysecret"
    hashed = hash_password(pw)
    assert hashed != pw
    assert verify_password(pw, hashed)
    assert not verify_password("wrong", hashed)

def test_create_and_decode_token():
    token = create_token(user_id=42)
    assert decode_token(token) == 42

def test_decode_invalid_token_returns_none():
    assert decode_token("not.a.token") is None
