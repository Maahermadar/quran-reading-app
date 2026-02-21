from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from ..db import database, models, schemas
from ..core import security
from datetime import timedelta
from ..utils.deps import get_current_user
import os
import shutil

router = APIRouter()

@router.post("/register", response_model=schemas.UserResponse)
def register(user_in: schemas.UserCreate, db: Session = Depends(database.get_db)):
    print(f"[REGISTER] Attempting registration for: {user_in.email}")
    try:
        user = db.query(models.User).filter(models.User.email == user_in.email).first()
        if user:
            raise HTTPException(
                status_code=400,
                detail="An account with this email already exists.",
            )
        
        hashed_password = security.get_password_hash(user_in.password)
        new_user = models.User(
            email=user_in.email,
            name=user_in.name,
            password_hash=hashed_password,
            lifetime_completions=0,
            is_cycle_completed=0,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        print(f"[REGISTER] Success - user id: {new_user.id}")
        return new_user
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"[REGISTER] CRITICAL ERROR: {type(e).__name__}: {e}")
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@router.post("/login", response_model=schemas.Token)
def login(db: Session = Depends(database.get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not security.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = security.create_access_token(subject=user.id)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.UserResponse)
def get_me(current_user: models.User = Depends(get_current_user)):
    # Add Cache-Control headers to prevent CDN or browser from caching user-specific responses
    response = JSONResponse(content={
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name,
        "avatar_url": current_user.avatar_url,
        "lifetime_completions": current_user.lifetime_completions,
        "is_cycle_completed": current_user.is_cycle_completed,
        "created_at": current_user.created_at.isoformat(),
    })
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    return response

@router.post("/avatar")
async def update_avatar(
    current_user: models.User = Depends(get_current_user),
    avatar: UploadFile = File(...),
    db: Session = Depends(database.get_db)
):
    # Validate file type
    if avatar.content_type not in ["image/jpeg", "image/png", "image/webp"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPG, PNG, and WEBP are allowed.")
    
    # Validate file size (2MB)
    MAX_SIZE = 2 * 1024 * 1024
    file_bytes = await avatar.read()
    if len(file_bytes) > MAX_SIZE:
        raise HTTPException(status_code=400, detail="File too large. Max size is 2MB.")
    
    # Save file
    file_ext = avatar.filename.split(".")[-1]
    filename = f"{current_user.id}.{file_ext}"
    upload_path = f"uploads/avatars/{filename}"
    
    with open(upload_path, "wb") as buffer:
        buffer.write(file_bytes)
    
    # Update user in DB
    avatar_url = f"/static/avatars/{filename}"
    current_user.avatar_url = avatar_url
    db.add(current_user)
    db.commit()
    
    return {"avatar_url": avatar_url}
