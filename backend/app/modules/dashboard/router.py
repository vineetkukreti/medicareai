from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.modules.dashboard import schemas
from app.modules.dashboard.service import dashboard_service
from app.modules.auth.models import User
from typing import List, Optional
from datetime import datetime, date

router = APIRouter()

@router.post("/health/upload")
async def upload_health_data(
    user_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload and parse Apple Health export XML file
    """
    return await dashboard_service.upload_health_data(db, user_id, file)

@router.get("/health/profile/{user_id}", response_model=schemas.HealthProfileResponse)
async def get_health_profile(user_id: int, db: Session = Depends(get_db)):
    """
    Get user's health profile
    """
    profile = dashboard_service.get_health_profile(db, user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Health profile not found")
    return profile

@router.get("/health/sleep/{user_id}", response_model=List[schemas.SleepRecordResponse])
async def get_sleep_records(
    user_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """
    Get sleep records for a user
    """
    return dashboard_service.get_sleep_records(db, user_id, start_date, end_date)

@router.get("/health/activity/{user_id}", response_model=List[schemas.ActivityRecordResponse])
async def get_activity_records(
    user_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """
    Get activity records for a user
    """
    return dashboard_service.get_activity_records(db, user_id, start_date, end_date)

@router.get("/health/vitals/{user_id}", response_model=List[schemas.VitalRecordResponse])
async def get_vital_records(
    user_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get vital records for a user
    """
    return dashboard_service.get_vital_records(db, user_id, start_date, end_date, limit)

@router.get("/health/dashboard/{user_id}", response_model=schemas.DashboardSummary)
async def get_dashboard_summary(user_id: int, db: Session = Depends(get_db)):
    """
    Get comprehensive dashboard summary with today's stats, week trends, and month averages
    """
    return dashboard_service.get_dashboard_summary(db, user_id)
