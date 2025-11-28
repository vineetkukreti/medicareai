from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

class HealthRecordCreate(BaseModel):
    record_type: str
    title: str
    description: str
    file_url: Optional[str] = None
    record_date: date

class HealthRecordResponse(HealthRecordCreate):
    id: int
    user_id: int
    created_at: datetime
    class Config:
        from_attributes = True
