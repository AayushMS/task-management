# Services Map

| Service | Type | Framework | Local Port | Depends On |
|---------|------|-----------|------------|------------|
| backend | Python API + static frontend | FastAPI + Uvicorn | 8000 | db, redis |
| db | PostgreSQL database | postgres:15 | 5432 | — |
| redis | Redis cache / token blacklist | redis:7-alpine | 6379 | — |

> Note: The frontend (vanilla HTML/CSS/JS in `frontend/`) is served as static files by the backend at `/`. There is no separate frontend deployment.

## Environment Variables Per Service

### backend
| Variable | Description | Source |
|----------|-------------|--------|
| `DATABASE_URL` | PostgreSQL connection string | Output of Neon setup (connection string) |
| `REDIS_URL` | Redis connection string | Output of Upstash setup (redis://... URL) |
| `SECRET_KEY` | JWT signing secret | Set manually — generate with `openssl rand -hex 32` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT token TTL in minutes | Set manually (e.g. `1440`) |

### db (local only — replaced by Neon in production)
| Variable | Description |
|----------|-------------|
| `POSTGRES_USER` | DB username |
| `POSTGRES_PASSWORD` | DB password |
| `POSTGRES_DB` | DB name |

### redis (local only — replaced by Upstash in production)
No env vars required for local Redis.
