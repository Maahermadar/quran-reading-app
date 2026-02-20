from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
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
    print(f"Registering user: {user_in.email}")
    print(f"Password length: {len(user_in.password)}")
    user = db.query(models.User).filter(models.User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    
    hashed_password = security.get_password_hash(user_in.password)
    new_user = models.User(
        email=user_in.email,
        name=user_in.name,
        password_hash=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Initialize lifetime stats
    stats = models.LifetimeStat(user_id=new_user.id, total_completions=0)
    db.add(stats)
    db.commit()
    
    return new_user

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
    return current_user

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
