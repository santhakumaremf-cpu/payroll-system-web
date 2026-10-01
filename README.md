# Payroll System - Modern Web Version

Migrated from original **VB6 + MS Access + Data Reports** (2013) to a modern full-stack web application.

## Tech Stack

| Layer       | Technology                              |
|-------------|-----------------------------------------|
| Backend     | Python 3.12 + FastAPI + SQLAlchemy      |
| Frontend    | React 19 + TypeScript + Tailwind CSS 4  |
| Database    | SQLite (dev) → easy switch to PostgreSQL|
| Auth        | JWT + bcrypt                            |
| Icons       | Lucide React                            |

## Project Structure

```
payroll-web/
├── backend/
│   ├── app/
│   │   ├── models/database.py      # SQLAlchemy models
│   │   ├── services/payroll_calculator.py
│   │   ├── routers/                # API endpoints
│   │   ├── schemas/                # Pydantic models
│   │   ├── core/                   # Config + Security
│   │   └── main.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/client.ts
│   │   ├── context/AuthContext.tsx
│   │   ├── pages/                  # Login, Dashboard, Employees...
│   │   ├── components/Layout.tsx
│   │   └── types/
│   └── package.json
├── docs/DATABASE_DESIGN.md
└── scripts/seed_data.py
```

## Quick Start

### 1. Backend

```bash
cd backend
pip install -r requirements.txt

PYTHONPATH=. uvicorn app.main:app --reload --port 8000
```

API Docs → http://localhost:8000/docs

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open → http://localhost:5173

### Default Logins

| Username | Password  | Role  |
|----------|-----------|-------|
| admin    | admin123  | Admin |
| khen     | khen123   | User  |

## Features

- [x] Modern database design
- [x] Payroll calculation engine
- [x] JWT Authentication
- [x] Employees CRUD
- [x] Positions CRUD
- [x] Process Payroll API
- [x] React Frontend
- [x] PDF Payslip generation
- [x] Vercel + Render deploy ready

## Deploy

See [docs/DEPLOY.md](docs/DEPLOY.md)

## Original System

- Author: Jhon Kenneth N. Carino (2013)
- Premiere Computer Learning Center
