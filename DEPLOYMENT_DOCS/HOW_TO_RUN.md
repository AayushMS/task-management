# How to Run Locally

## Prerequisites

- Python 3.12
- Docker & Docker Compose (recommended for local dev)

## Install Dependencies

```bash
# Backend only (without Docker)
cd backend
pip install -r requirements.txt
```

## Environment Variables

Copy `.env.example` to `.env` and fill in values:

- `DATABASE_URL` — PostgreSQL connection string (e.g. `postgresql://taskuser:taskpass@localhost:5432/taskdb`)
- `REDIS_URL` — Redis connection string (e.g. `redis://localhost:6379/0`)
- `SECRET_KEY` — Secret key for JWT signing (min 32 chars)
- `ACCESS_TOKEN_EXPIRE_MINUTES` — JWT token lifetime in minutes (default: 1440 = 24h)

## Start Services (in order)

### Option A: Docker Compose (recommended)

```bash
# From project root — starts DB, Redis, and backend together
docker compose up --build
```

### Option B: Manual

```bash
# 1. Start PostgreSQL (port 5432)
docker run -d -e POSTGRES_USER=taskuser -e POSTGRES_PASSWORD=taskpass -e POSTGRES_DB=taskdb -p 5432:5432 postgres:15

# 2. Start Redis (port 6379)
docker run -d -p 6379:6379 redis:7-alpine

# 3. Start backend (from project root, so frontend static files are accessible)
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Local URLs

- Backend API: http://localhost:8000
- Frontend (served by backend): http://localhost:8000/
- API docs (Swagger): http://localhost:8000/docs
