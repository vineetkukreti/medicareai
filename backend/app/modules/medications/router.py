from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.modules.medications import schemas
from app.modules.medications.service import medication_service
from app.modules.auth.models import User
from typing import List

router = APIRouter()

@router.post("/medications", response_model=schemas.MedicationResponse)
async def create_medication(
    medication: schemas.MedicationCreate, 
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """
    Add a new medication for a user
    """
    return medication_service.create_medication(db, medication, current_user.id, background_tasks)

@router.get("/medications", response_model=List[schemas.MedicationResponse])
async def get_user_medications(
    active_only: bool = True, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all medications for the authenticated user
    """
    return medication_service.get_user_medications(db, current_user.id, active_only)

@router.get("/medications/{medication_id}", response_model=schemas.MedicationResponse)
async def get_medication(
    medication_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific medication by ID
    """
    medication = medication_service.get_medication_by_id(db, medication_id)
    if not medication:
        raise HTTPException(status_code=404, detail="Medication not found")
    
    # Check ownership
    if medication.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return medication

@router.put("/medications/{medication_id}")
async def update_medication(
    medication_id: int, 
    medication: schemas.MedicationCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update a medication
    """
    # Check ownership
    db_medication = medication_service.get_medication_by_id(db, medication_id)
    if not db_medication:
        raise HTTPException(status_code=404, detail="Medication not found")
    if db_medication.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    updated_medication = medication_service.update_medication(db, medication_id, medication)
    return updated_medication

@router.delete("/medications/{medication_id}")
async def delete_medication(
    medication_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Deactivate a medication
    """
    # Check ownership
    db_medication = medication_service.get_medication_by_id(db, medication_id)
    if not db_medication:
        raise HTTPException(status_code=404, detail="Medication not found")
    if db_medication.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    medication_service.delete_medication(db, medication_id, current_user.id)
    return {"message": "Medication deactivated successfully"}
