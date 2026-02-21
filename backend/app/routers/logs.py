from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import database, models, schemas
from ..utils.deps import get_current_user
from ..services import calc
from typing import List

router = APIRouter()

@router.post("/", response_model=schemas.ReadingLogResponse)
def create_reading_log(
    log_in: schemas.ReadingLogCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Step 0 — Strict Validation
    # Determine effective start page
    last_log = db.query(models.ReadingLog).filter(models.ReadingLog.user_id == current_user.id).order_by(models.ReadingLog.created_at.desc()).first()
    
    # Effective starting page for validation
    effective_start = 1
    if last_log and not current_user.is_cycle_completed:
        effective_start = last_log.end_page

    if log_in.end_page < 1 or log_in.end_page > 604:
        raise HTTPException(status_code=400, detail="Page must be between 1 and 604")
        
    if log_in.end_page < effective_start:
        raise HTTPException(status_code=400, detail=f"End page cannot be less than last finished page ({effective_start})")

    # Step 1 — Detect completion FROM THIS LOG ONLY
    completed = log_in.end_page == 604

    # Create the log first (not yet committed)
    new_log = models.ReadingLog(
        user_id=current_user.id,
        start_page=log_in.start_page,
        end_page=log_in.end_page,
        completion_counted=0  # Default: not counted
    )
    db.add(new_log)

    # Step 2 — Increment only if this is a completion AND not already counted
    if completed and new_log.completion_counted == 0:
        current_user.lifetime_completions += 1
        current_user.is_cycle_completed = True
        new_log.completion_counted = 1  # Mark this log as counted — idempotency guard

    # Step 3 — If NOT a completion but previous cycle was completed, reset the flag
    elif not completed and current_user.is_cycle_completed:
        current_user.is_cycle_completed = False

    db.commit()
    db.refresh(new_log)
    return new_log


@router.get("/last-page")
def get_last_page(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    last_log = (
        db.query(models.ReadingLog)
        .filter(models.ReadingLog.user_id == current_user.id)
        .order_by(models.ReadingLog.created_at.desc())
        .first()
    )
    if not last_log:
        return {"last_page": 1}
    
    # If the user finished Exactly on page 604, the next cycle starts at page 1
    if last_log.end_page == 604:
        return {"last_page": 1}
        
    return {"last_page": last_log.end_page}
