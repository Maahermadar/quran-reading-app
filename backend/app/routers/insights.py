from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import database, models
from ..services import calc
from ..utils.deps import get_current_user
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/")
def get_insights(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Fetch all logs for the user
    logs = db.query(models.ReadingLog).filter(
        models.ReadingLog.user_id == current_user.id
    ).order_by(models.ReadingLog.created_at.asc()).all()
    
    log_dates = [log.created_at for log in logs]
    streak = calc.calculate_streak(log_dates)
    longest_streak = calc.calculate_longest_streak(log_dates)
    
    avg_7_days = calc.calculate_average_pages(logs, days=7)
    daily_stats = calc.get_daily_reading_stats(logs, days=7)
    weekly_total = sum(d["pages"] for d in daily_stats)
    
    best_time = calc.get_best_reading_time(logs)
    
    # Simple forecast: next 100 pages
    est_days_100 = round(100 / avg_7_days, 1) if avg_7_days > 0 else "N/A"
    
    return {
        "streak": streak,
        "longest_streak": longest_streak,
        "avg_pages_7_days": avg_7_days,
        "weekly_total": weekly_total,
        "daily_stats": daily_stats,
        "best_time": best_time,
        "est_days_for_100_pages": est_days_100,
        "total_logs": len(logs)
    }
