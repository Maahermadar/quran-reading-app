from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import database, models
from ..utils.deps import get_current_user
from ..services import calc
from sqlalchemy import func

router = APIRouter()

@router.get("/")
def get_progress(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    last_log = db.query(models.ReadingLog).filter(models.ReadingLog.user_id == current_user.id).order_by(models.ReadingLog.created_at.desc()).first()
    
    current_page = last_log.end_page if last_log else 1
    juz = calc.get_juz_from_page(current_page)
    progress_pct = calc.calculate_progress_percentage(current_page)
    
    stats = db.query(models.LifetimeStat).filter(models.LifetimeStat.user_id == current_user.id).first()
    completions = stats.total_completions if stats else 0
    
    return {
        "current_page": current_page,
        "juz": juz,
        "progress_percentage": progress_pct,
        "pages_left": 600 - current_page if current_page <= 600 else 0,
        "lifetime_completions": completions,
        "is_cycle_completed": bool(stats.is_cycle_completed) if stats else False
    }
