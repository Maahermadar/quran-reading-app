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
    
    # Madani Mushaf Logic
    from ..services import surah_service
    juz = surah_service.get_juz_for_page(current_page)
    surah_info = surah_service.get_surah_info_for_page(current_page)
    
    progress_pct = calc.calculate_progress_percentage(current_page)
    
    return {
        "current_page": current_page,
        "juz": juz,
        "surah_name_en": surah_info["name_en"] if surah_info else "N/A",
        "surah_name_ar": surah_info["name_ar"] if surah_info else "N/A",
        "progress_percentage": progress_pct,
        "pages_left": 604 - current_page if current_page <= 604 else 0,
        "lifetime_completions": current_user.lifetime_completions,
        "is_cycle_completed": bool(current_user.is_cycle_completed)
    }
