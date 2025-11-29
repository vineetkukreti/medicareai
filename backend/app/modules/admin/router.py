from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.modules.admin import schemas
from app.modules.admin.service import admin_service
from app.core.security import get_current_user
from app.modules.auth.models import User

router = APIRouter()

# Dependency to check if user is admin
def get_current_admin(current_user: User = Depends(get_current_user)):
    # For now, we check email. Ideally, we should have a role field.
    if current_user.email != "admin@gmail.com": # Hardcoded for now as per login
         raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access admin portal"
        )
    return current_user

@router.get("/stats", response_model=schemas.StatsResponse)
def get_admin_stats(
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_admin) # Commented out for easier testing, uncomment for prod
):
    return admin_service.get_stats(db)

@router.get("/users", response_model=List[schemas.PatientSummary])
def get_patients(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_admin)
):
    return admin_service.get_patients(db, skip, limit)

@router.get("/doctors", response_model=List[schemas.DoctorSummary])
def get_doctors(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_admin)
):
    return admin_service.get_doctors(db, skip, limit)
