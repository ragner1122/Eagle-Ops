# EAGLE SupportOps

Tier-1 support operations demo app covering ticketing, triage, runbooks, knowledge base, and telemetry.

## Implementation Plan

### Phase 1: Scaffold & Architecture
- Stand up Next.js frontend and FastAPI backend folders.
- Configure SQLite database with SQLAlchemy models.
- Add auth with email/password and roles (Admin, Analyst).

### Phase 2: MVP Features
- Seed demo data for tickets, runbooks, knowledge base, telemetry.
- Implement read-only API endpoints for each domain.
- Build the `/` dashboard with enterprise light UI.

### Phase 3: Extension Hooks
- Prepare backend for Postgres by keeping SQLAlchemy models abstracted.
- Leave room for additional CRUD endpoints and role-based controls.

## Repo Structure

```
.
├── backend
│   ├── app
│   │   ├── auth.py
│   │   ├── db.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── routers
│   │   │   ├── knowledge.py
│   │   │   ├── runbooks.py
│   │   │   ├── telemetry.py
│   │   │   └── tickets.py
│   │   ├── schemas.py
│   │   └── seed.py
│   └── requirements.txt
├── frontend
│   ├── app
│   │   ├── globals.css
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── next-env.d.ts
│   ├── next.config.js
│   ├── package.json
│   └── tsconfig.json
└── README.md
```

## Setup

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Health check:

```bash
curl http://localhost:8000/health
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

## Demo Accounts

- Admin: `admin@eagleops.io` / `AdminPass123`
- Analyst: `analyst@eagleops.io` / `AnalystPass123`
