from fastapi import APIRouter, Depends, HTTPException
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
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """
    Add a new medication for a user
    """
    return medication_service.create_medication(db, medication, current_user.id)

@router.get("/medications/{user_id}", response_model=List[schemas.MedicationResponse])
async def get_user_medications(
    user_id: int, 
    active_only: bool = True, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # Added auth check
):
    """
    Get all medications for a user
    """
    # Ensure user can only access their own medications or admin
    if user_id != current_user.id:
         raise HTTPException(status_code=403, detail="Access denied")
         
    return medication_service.get_user_medications(db, user_id, active_only)

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

    medication_service.delete_medication(db, medication_id)
    return {"message": "Medication deactivated successfully"}
