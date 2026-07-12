# Task Management

Full-stack task list app: register/login, then create, check off, and delete
your own tasks. Each user only sees their own tasks.

## Live App

https://task-management-backend-kgqn.onrender.com

Frontend is served as static files by the backend (no separate frontend deployment).
Free-tier Render service — spins down after 15 min of inactivity, so the first
request after a while takes ~30s to cold-start.

## Features

- Register / login with JWT auth
- Logout revokes the token via a Redis blacklist (not just a client-side discard)
- Per-user task CRUD (create, toggle done, delete)

## Tech Stack

- Backend: Python / FastAPI
- Frontend: Vanilla HTML/CSS/JS (served as static files, no build step)
- Database: PostgreSQL (Neon in production)
- Cache: Redis (Upstash in production, used for the JWT blacklist)
- Deployment: Render, via the root `Dockerfile`

## Running Locally

```bash
docker compose up --build
```

This starts Postgres, Redis, and the backend (which also serves the frontend)
together. Then open http://localhost:8000. See
[`DEPLOYMENT_DOCS/HOW_TO_RUN.md`](DEPLOYMENT_DOCS/HOW_TO_RUN.md) for the
manual (non-Docker) setup and required environment variables.

## Deployment

- **App (frontend + backend):** Render (free tier)
- **Database:** Neon PostgreSQL (`wandering-star-17513992`)
- **Redis:** Upstash (`bright-hagfish-4552.upstash.io`)
- **CI/CD:** GitHub Actions (auto-deploy on push + health check every 6 hours)

See [`DEPLOYMENT_DOCS/`](DEPLOYMENT_DOCS/) for the full deployment plan, service map, and log.
