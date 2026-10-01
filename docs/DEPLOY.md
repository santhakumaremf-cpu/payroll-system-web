# Deployment Guide

## Frontend → Vercel
## Backend → Render

See README for full instructions.

### Backend (Render)
- Root: backend
- Build: pip install -r requirements.txt
- Start: uvicorn app.main:app --host 0.0.0.0 --port $PORT

### Frontend (Vercel)
- Root: frontend
- Env: VITE_API_URL=https://your-backend.onrender.com/api/v1
