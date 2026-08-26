from fastapi import APIRouter, Depends, HTTPException, status
from Medication_tracker.database import get_db
from Medication_tracker.models import User
from Medication_tracker.schemas import ( 
    StreakResponse
)
from Medication_tracker.crud import (
    get_or_create_streak)
from sqlalchemy.orm import Session
from Medication_tracker.core.dependencies import get_current_user



router = APIRouter(prefix="/streaks", tags=["MEDICATIONS_STREAKS"])


@router.get("/{med_id}", response_model=StreakResponse, status_code=status.HTTP_200_OK, description="Get Streak stats")
def streak(med_id: int, db:Session=Depends(get_db), current_user:User=Depends(get_current_user)):
    db_streak = get_or_create_streak(db, med_id, current_user.id)
    
    return db_streak