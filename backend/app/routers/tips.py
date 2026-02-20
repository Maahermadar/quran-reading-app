from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import database, models
from ..utils.deps import get_current_user
import random

router = APIRouter()

TIPS_POOL = [
    "Consistency is key. Try reading at the same time every day.",
    "Start with just one page after Fajr. It sets a barakah tone for the day.",
    "Focus on quality over quantity. Reflect on one verse even if you read many.",
    "Listening to your favorite reciter can help you improve your pace and Tajweed.",
    "Use a physical mushaf when possible; it reduces digital distractions.",
    "Set small reachable goals to stay motivated.",
    "Review what you read at the end of the week to retain more."
]

@router.get("/")
def get_tips(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    # For now, return a random tip and a few featured ones
    return {
        "daily_tip": random.choice(TIPS_POOL),
        "featured": random.sample(TIPS_POOL, 3)
    }
