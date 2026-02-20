from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import database, models, schemas
from ..utils.deps import get_current_user
from ..services import calc
from datetime import datetime
from sqlalchemy import func
import math

router = APIRouter()

@router.post("/", response_model=schemas.GoalResponse)
def create_goal(
    goal_in: schemas.GoalCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Cancel previous active goals
    db.query(models.Goal).filter(
        models.Goal.user_id == current_user.id,
        models.Goal.status == models.GoalStatus.active
    ).update({"status": models.GoalStatus.cancelled})
    
    new_goal = models.Goal(
        user_id=current_user.id,
        target_pages=goal_in.target_pages,
        target_days=goal_in.target_days,
        start_at=datetime.utcnow(),
        status=models.GoalStatus.active
    )
    db.add(new_goal)
    db.commit()
    db.refresh(new_goal)
    return new_goal

@router.get("/active")
def get_active_goal(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    goal = db.query(models.Goal).filter(
        models.Goal.user_id == current_user.id,
        models.Goal.status == models.GoalStatus.active
    ).first()
    
    if not goal:
        return {"has_goal": False}
    
    # Calculate pages done since goal start
    logs = db.query(models.ReadingLog).filter(
        models.ReadingLog.user_id == current_user.id,
        models.ReadingLog.created_at >= goal.start_at
    ).all()
    
    pages_done = sum(calc.calculate_pages_read(l.start_page, l.end_page) for l in logs)
    
    # Time calculations
    now = datetime.utcnow()
    deadline = goal.start_at.timestamp() + (goal.target_days * 86400)
    remaining_seconds = max(0, deadline - now.timestamp())
    remaining_days = math.ceil(remaining_seconds / 86400)
    
    remaining_pages = max(0, goal.target_pages - pages_done)
    progress_pct = min(100, round((pages_done / goal.target_pages) * 100, 1))
    
    return {
        "has_goal": True,
        "target_pages": goal.target_pages,
        "target_days": goal.target_days,
        "pages_done": pages_done,
        "remaining_pages": remaining_pages,
        "remaining_days": remaining_days,
        "pages_left": remaining_pages, # Sync with home.js
        "days_left": remaining_days,   # Sync with home.js
        "progress_percentage": progress_pct,
        "daily_needed": math.ceil(remaining_pages / max(1, remaining_days))
    }
