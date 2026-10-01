"""
Payroll System - FastAPI Backend
Modern web version of the original VB6 Payroll System
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models.database import init_db
from app.core.config import settings
from app.routers import auth, employees, positions, dtr, payroll

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Modern web version of VB6 Payroll System (2013)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "https://*.vercel.app",
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_db()


app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(employees.router, prefix=settings.API_V1_STR)
app.include_router(positions.router, prefix=settings.API_V1_STR)
app.include_router(dtr.router, prefix=settings.API_V1_STR)
app.include_router(payroll.router, prefix=settings.API_V1_STR)


@app.get("/")
def root():
    return {
        "message": "Payroll System API is running",
        "version": "1.0.0",
        "docs": "/docs",
        "api_prefix": settings.API_V1_STR,
    }


@app.get("/health")
def health():
    return {"status": "ok"}
