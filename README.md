# Filmstagram

A full-stack social app for sharing movie reviews—think Instagram, but every post is anchored to a film from a curated catalog backed by [The Movie Database (TMDB)](https://www.themoviedb.org/).

Built as a portfolio project to demonstrate end-to-end product development: relational data modeling, authenticated REST APIs, third-party integration, and a responsive React UI.

---

## Highlights (for reviewers)

- **Monorepo** with a **FastAPI** backend and **Next.js (App Router)** frontend, communicating over a typed JSON API.
- **JWT authentication** with protected routes on the client and dependency-injected auth on the server.
- **PostgreSQL** schema with **Alembic** migrations; normalized movie metadata (genres, cast, crew) imported from TMDB.
- **Social graph**: follow/unfollow, user search and suggestions, and a **paginated feed** of posts from followed users.
- **Posts** tie free-text reviews (plus optional fields) to rich **movie previews** (poster, year, directors, top cast).
- Practical frontend patterns: debounced search, scroll-contained feed layout, shared API client with empty/204 response handling.

---

## Features

| Area | Status |
|------|--------|
| Register / login | Done |
| Create post (movie search + preview) | Done |
| Feed (newest first, 30 per page, load more) | Done |
| Follow / unfollow, user search, suggestions | Done |
| Local movie search & TMDB import pipeline | Done |
| Discover & profile pages | Placeholder UI |

---

## Tech stack

**Backend**

- Python 3, FastAPI, Pydantic v2, SQLAlchemy 2
- PostgreSQL, Alembic, psycopg
- JWT (`python-jose`), bcrypt password hashing
- HTTPX for TMDB API calls

**Frontend**

- Next.js 16, React 19, TypeScript
- Tailwind CSS v4
- Client-side auth context + route protection

**Infrastructure**

- Docker Compose for local PostgreSQL

---

## Architecture (high level)

```
┌─────────────────┐     HTTPS / JSON      ┌─────────────────┐
│  Next.js (UI)   │ ◄──────────────────► │  FastAPI API    │
│  App Router     │     Bearer JWT         │  + SQLAlchemy   │
└─────────────────┘                       └────────┬────────┘
                                                   │
                                          ┌────────▼────────┐
                                          │   PostgreSQL    │
                                          └────────┬────────┘
                                                   │
                                          ┌────────▼────────┐
                                          │   TMDB API      │
                                          │ (import/search) │
                                          └─────────────────┘
```

**Domain concepts**

- **Users** — accounts with profiles; **Follow** many-to-many via `follows`.
- **Movies** — stored locally after TMDB import; cast/crew trimmed for previews (e.g. top cast, directors).
- **Posts** — user-authored reviews linked to a `movie_id`; feed query joins follows and orders by `created_at`.

Interactive API docs: `http://localhost:8000/docs` when the backend is running.

---

## Repository layout

```
filmstagram/
├── backend/          # FastAPI app, models, services, Alembic, scripts
├── frontend/         # Next.js app (routes, components, lib/api)
└── docker-compose.yml
```

---

## Getting started

### Prerequisites

- Node.js 20+ and npm
- Python 3.11+ (3.13 tested in development)
- Docker (for PostgreSQL)
- A [TMDB API key](https://www.themoviedb.org/settings/api)

### 1. Database

From the repo root:

```bash
docker compose up -d
```

Default connection (matches `docker-compose.yml`):

- Database: `movie_db`
- User: `movie_user`
- Password: `password`
- Port: `5432`

### 2. Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # then edit with your secrets
```

Run migrations and optional seed data:

```bash
alembic upgrade head
python -m app.scripts.seed_users      # demo users steve1–steve10
# Import movies as needed, e.g.:
# python -m app.scripts.import_movie 550
```

Start the API:

```bash
uvicorn app.main:app --reload
```

API base URL: `http://localhost:8000`

### 3. Frontend

```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

Open `http://localhost:3000`, register or log in with a seeded user (e.g. `steve1@example.com` / `password123`).

---

## Environment variables

See `backend/.env.example` and `frontend/.env.example` for required values.

---

## Design decisions (brief)

- **Local movie catalog** — Search and previews hit the database, not TMDB on every request; imports keep the app fast and offline-friendly for demos.
- **Feed pagination** — `limit` + `offset` with `has_more` / `next_offset` keeps the first paint small and supports “load more” without infinite-scroll complexity.
- **Layered backend** — Routers → services → models/schemas separates HTTP concerns from business logic and eases testing and extension.
- **Protected app shell** — `(app)` routes sit behind auth; public login/register live under `(auth)`.

---

## Possible extensions

- Discover page (genre/browse), profile pages (user posts & follows)
- Include own posts in feed; eager-loading optimizations on hot paths
- Image uploads for avatars; rate limiting on auth and search
- Deployment (e.g. API on Railway/Fly, frontend on Vercel, managed Postgres)

---

## Author

**Steven Nelson**

---

## License

This project is for demonstration purposes. TMDB data and images are subject to [TMDB terms of use](https://www.themoviedb.org/documentation/api/terms-of-use). Add an explicit license (e.g. MIT) here if you open-source the code.
