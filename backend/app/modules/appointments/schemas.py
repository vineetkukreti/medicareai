from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date, time

class TimeSlot(BaseModel):
    """Represents an available time slot"""
    start_time: str  # Format: "09:00"
    end_time: str    # Format: "09:30"
    is_available: bool = True


class AppointmentCreate(BaseModel):
    doctor_id: int
    appointment_date: date
    start_time: time
    end_time: time
    reason: Optional[str] = None
    notes: Optional[str] = None


class AppointmentUpdate(BaseModel):
    status: Optional[str] = None  # pending, confirmed, completed, cancelled
    notes: Optional[str] = None


class AppointmentResponse(BaseModel):
    id: int
    user_id: int
    doctor_id: Optional[int]
    appointment_date: date
    start_time: time
    end_time: time
    reason: Optional[str]
    status: str
    notes: Optional[str] = None
    meeting_link: Optional[str] = None
    created_at: datetime
    created_via: str
    
    # Include doctor and patient info
    doctor_name: Optional[str] = None
    patient_name: Optional[str] = None

    class Config:
        from_attributes = True


class PatientInfo(BaseModel):
    """Patient information for doctors to view"""
    id: int
    full_name: str
    email: str
    phone_number: Optional[str]
    date_of_birth: Optional[date]
    gender: Optional[str]

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
