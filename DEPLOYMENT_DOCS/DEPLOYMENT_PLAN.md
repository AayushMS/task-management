# Deployment Plan

## Detected Services

- **backend** — Python API server (FastAPI/Uvicorn), also serves the static frontend
- **db** — PostgreSQL 15 database
- **redis** — Redis 7 (used for JWT token blacklist on logout)
- **frontend** — Vanilla HTML/CSS/JS static files (embedded in backend — no separate service)

## Recommended Platforms

| Service | Platform | Reason | Free Tier Limits |
|---------|----------|--------|-----------------|
| backend | Render | Python/FastAPI server with Dockerfile; persistent process needed for Redis connection | 750 hrs/month; spins down after 15 min inactivity |
| db (PostgreSQL) | Neon | Project only needs a database — no auth/storage features needed from Supabase | 0.5 GB storage, 1 project |
| redis | Upstash | Redis detected in requirements.txt and REDIS_URL in .env.example | 10,000 commands/day, 256 MB |
| frontend | (embedded in backend) | Static files served directly by FastAPI — no separate deploy needed | N/A |

## Free Tier Warnings

- **Render**: Free services spin down after 15 minutes of inactivity. Cold start on next request takes ~30 seconds.
- **Neon**: Free tier includes 0.5 GB storage and 1 project. Branches are paused after extended inactivity.
- **Upstash**: Free tier allows 10,000 Redis commands per day.

## Deployment Order

1. **db** (PostgreSQL) → Neon
2. **redis** → Upstash
3. **backend** (FastAPI + static frontend) → Render

## Required Accounts

- [Neon](https://neon.tech) — for PostgreSQL
- [Upstash](https://upstash.com) — for Redis
- [Render](https://render.com) — for backend API

## Environment Variable Wiring

After deploying **Neon** (database):
- Set `DATABASE_URL` on **backend (Render)** using the connection string from Neon dashboard
  - Use the **pooled connection string** with `?sslmode=require` appended

After deploying **Upstash** (Redis):
- Set `REDIS_URL` on **backend (Render)** using the `redis://...` URL from Upstash console

After deploying **backend** (Render):
- No further wiring needed — the frontend is served at the root of the same Render URL
- Set `SECRET_KEY` on Render to a securely generated value: `openssl rand -hex 32`
- Set `ACCESS_TOKEN_EXPIRE_MINUTES` on Render (e.g. `1440`)
