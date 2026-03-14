# Task Management

Full-stack task management application with real-time updates.

## Live App

https://task-management-backend-kgqn.onrender.com

Frontend is served as static files by the backend (no separate frontend deployment).

## Deployment

- **App (frontend + backend):** Render (free tier)
- **Database:** Neon PostgreSQL (`wandering-star-17513992`)
- **Redis:** Upstash (`bright-hagfish-4552.upstash.io`)
- **CI/CD:** GitHub Actions (auto-deploy on push + health check every 6 hours)

## Tech Stack

- Backend: Python / FastAPI
- Frontend: Vanilla HTML/CSS/JS (served as static files)
- Database: PostgreSQL (Neon)
- Cache: Redis (Upstash)
- Deployment: Render
