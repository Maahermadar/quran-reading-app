import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from .db import database, models
from .routers import auth, logs, progress, goals, insights, tips

app = FastAPI(title="Quran Reading Tracker API")

# Ensure upload directory exists
UPLOAD_DIR = "uploads/avatars"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Mount static files (Disabled - avatars moved to Cloudflare Assets)
# app.mount("/static", StaticFiles(directory="uploads"), name="static")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables (for local dev without alembic first, but plan says use alembic)
# models.Base.metadata.create_all(bind=database.engine)

@app.get("/")
async def root():
    return {"message": "Welcome to Quran Tracker API"}

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(logs.router, prefix="/logs", tags=["logs"])
app.include_router(progress.router, prefix="/progress", tags=["progress"])
app.include_router(goals.router, prefix="/goals", tags=["goals"])
app.include_router(insights.router, prefix="/insights", tags=["insights"])
app.include_router(tips.router, prefix="/tips", tags=["tips"])
