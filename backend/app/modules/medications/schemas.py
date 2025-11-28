from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

class MedicationCreate(BaseModel):
    medication_name: str
    dosage: str
    frequency: str
    start_date: date
    end_date: Optional[date] = None
    notes: Optional[str] = None

class MedicationResponse(MedicationCreate):
    id: int
    user_id: int
    is_active: bool
    created_at: datetime
    class Config:
        from_attributes = True
