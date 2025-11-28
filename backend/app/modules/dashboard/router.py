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

@router.get("/health/profile", response_model=schemas.HealthProfileResponse)
async def get_health_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get health profile for authenticated user
    """
    profile = dashboard_service.get_health_profile(db, current_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Health profile not found")
    return profile

@router.get("/health/sleep", response_model=List[schemas.SleepRecordResponse])
async def get_sleep_records(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 30
):
    """
    Get sleep records for authenticated user
    """
    return dashboard_service.get_sleep_records(db, current_user.id, limit)

@router.get("/health/activity", response_model=List[schemas.ActivityRecordResponse])
async def get_activity_records(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 30
):
    """
    Get activity records for authenticated user
    """
    return dashboard_service.get_activity_records(db, current_user.id, limit)

@router.get("/health/vitals", response_model=List[schemas.VitalRecordResponse])
async def get_vital_records(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 30
):
    """
    Get vital records for authenticated user
    """
    return dashboard_service.get_vital_records(db, current_user.id, limit)

@router.get("/health/dashboard", response_model=schemas.DashboardSummary)
async def get_dashboard_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get comprehensive dashboard summary for authenticated user
    """
    return dashboard_service.get_dashboard_summary(db, current_user.id)
