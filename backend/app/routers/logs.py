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
    # Step 1 — Detect completion FROM THIS LOG ONLY
    # A log is a completion if: end_page < start_page (wrap-around) OR end_page == 600
    completed = (
        log_in.end_page < log_in.start_page
        or log_in.end_page == 600
    )

    # Create the log first (not yet committed)
    new_log = models.ReadingLog(
        user_id=current_user.id,
        start_page=log_in.start_page,
        end_page=log_in.end_page,
        completion_counted=0  # Default: not counted
    )
    db.add(new_log)

    # Get or create lifetime stats
    stats = db.query(models.LifetimeStat).filter(
        models.LifetimeStat.user_id == current_user.id
    ).first()
    if not stats:
        stats = models.LifetimeStat(
            user_id=current_user.id,
            total_completions=0,
            is_cycle_completed=0
        )
        db.add(stats)

    # Step 2 — Increment only if this is a completion AND not already counted
    if completed and new_log.completion_counted == 0:
        stats.total_completions += 1
        stats.is_cycle_completed = 1
        new_log.completion_counted = 1  # Mark this log as counted — idempotency guard

    # Step 3 — If NOT a completion but previous cycle was completed, reset the flag
    elif not completed and stats.is_cycle_completed == 1:
        stats.is_cycle_completed = 0

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
    
    # If the user finished Exactly on page 600, the next cycle starts at page 1
    if last_log.end_page == 600:
        return {"last_page": 1}
        
    return {"last_page": last_log.end_page}
