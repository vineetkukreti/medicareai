from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AppointmentCreate(BaseModel):
    doctor_name: str
    specialty: str
    appointment_date: datetime
    reason: str
    notes: Optional[str] = None

class AppointmentResponse(AppointmentCreate):
    id: int
    user_id: int
    status: str
    created_at: datetime
    class Config:
        from_attributes = True

class DoctorScheduleCreate(BaseModel):
    doctor_name: str
    specialty: str
    day_of_week: int  # 0-6
    start_time: str  # "09:00"
    end_time: str  # "17:00"
    slot_duration: int = 30

class DoctorScheduleResponse(DoctorScheduleCreate):
    id: int
    is_available: bool
    created_at: datetime
    class Config:
        from_attributes = True

class AvailableSlot(BaseModel):
    doctor_name: str
    specialty: str
    date: str
    time: str
    datetime_iso: str
