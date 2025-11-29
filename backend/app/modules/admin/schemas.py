from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class StatsResponse(BaseModel):
    total_patients: int
    total_doctors: int
    total_appointments: int
    total_revenue: float
    pending_doctors: int
    active_patients: int

class PatientSummary(BaseModel):
    id: int
    full_name: Optional[str]
    email: str
    created_at: datetime
    is_active: bool = True

class DoctorSummary(BaseModel):
    id: int
    full_name: str
    email: str
    specialization: str
    experience_years: int
    is_verified: bool
    rating: float
    consultation_fee: float
    created_at: datetime

class VerifyDoctorRequest(BaseModel):
    is_verified: bool
