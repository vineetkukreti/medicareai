from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas import MedicationCreate, MedicationResponse
from app.models import Medication
from typing import List
from app.services.rag_service import rag_service

router = APIRouter()

@router.post("/medications", response_model=MedicationResponse)
async def create_medication(medication: MedicationCreate, user_id: int, db: Session = Depends(get_db)):
    """
    Add a new medication for a user
    """
    db_medication = Medication(**medication.dict(), user_id=user_id)
    db.add(db_medication)
    db.commit()
    db.refresh(db_medication)
    
    # Trigger RAG ingestion
    try:
        content = f"Medication: {db_medication.medication_name}, Dosage: {db_medication.dosage}, Frequency: {db_medication.frequency}, Start Date: {db_medication.start_date}, Notes: {db_medication.notes}"
        rag_service.upsert_data(
            user_id=user_id,
            data_type="medication",
            content=content,
            metadata={"medication_id": db_medication.id}
        )
    except Exception as e:
        print(f"Error triggering RAG ingestion: {e}")
        
    return db_medication

@router.get("/medications/{user_id}", response_model=List[MedicationResponse])
async def get_user_medications(user_id: int, active_only: bool = True, db: Session = Depends(get_db)):
    """
    Get all medications for a user
    """
    query = db.query(Medication).filter(Medication.user_id == user_id)
    if active_only:
        query = query.filter(Medication.is_active == True)
    medications = query.all()
    return medications

@router.put("/medications/{medication_id}")
async def update_medication(medication_id: int, medication: MedicationCreate, db: Session = Depends(get_db)):
    """
    Update a medication
    """
    db_medication = db.query(Medication).filter(Medication.id == medication_id).first()
    if not db_medication:
        raise HTTPException(status_code=404, detail="Medication not found")
    
    for key, value in medication.dict().items():
        setattr(db_medication, key, value)
    
    db.commit()
    db.refresh(db_medication)
    return db_medication

@router.delete("/medications/{medication_id}")
async def delete_medication(medication_id: int, db: Session = Depends(get_db)):
    """
    Deactivate a medication
    """
    db_medication = db.query(Medication).filter(Medication.id == medication_id).first()
    if not db_medication:
        raise HTTPException(status_code=404, detail="Medication not found")
    
    db_medication.is_active = False
    db.commit()
    return {"message": "Medication deactivated successfully"}
