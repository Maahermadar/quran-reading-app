import os
import re
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware
from .db import database, models
from .routers import auth, logs, progress, goals, insights, tips

app = FastAPI(title="Quran Reading Tracker API")

ALLOWED_ORIGIN_PATTERN = re.compile(
    r"^https://.*\.mhr01\.workers\.dev$|^http://localhost(:\d+)?$|^http://127\.0\.0\.1(:\d+)?$"
)

class CORSHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        origin = request.headers.get("origin", "")
        
        # Handle preflight OPTIONS request
        if request.method == "OPTIONS":
            response = Response()
            if ALLOWED_ORIGIN_PATTERN.match(origin):
                response.headers["Access-Control-Allow-Origin"] = origin
                response.headers["Access-Control-Allow-Credentials"] = "true"
                response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
                response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type, Accept"
            return response
        
        response = await call_next(request)
        
        if ALLOWED_ORIGIN_PATTERN.match(origin):
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
            response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type, Accept"
        
        return response

app.add_middleware(CORSHandlerMiddleware)

# Ensure upload directory exists
UPLOAD_DIR = "uploads/avatars"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="uploads"), name="static")

@app.on_event("startup")
async def startup_event():
    print("\n" + "="*50)
    print("BACKEND STARTED - CUSTOM CORS MIDDLEWARE ACTIVE")
    print("="*50 + "\n")

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
