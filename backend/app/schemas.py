from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, date

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    class Config:
        from_attributes = True

class UserResponse(UserBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    address: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None

class UserProfileResponse(BaseModel):
    id: int
    email: str
    full_name: Optional[str]
    phone_number: Optional[str]
    date_of_birth: Optional[date]
    gender: Optional[str]
    address: Optional[str]
    emergency_contact_name: Optional[str]
    emergency_contact_phone: Optional[str]
    created_at: datetime
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    email: str
    full_name: Optional[str] = None

class ContactCreate(BaseModel):
    name: str
    email: EmailStr
    message: str

class Contact(ContactCreate):
    id: int
    class Config:
        from_attributes = True

class ContactResponse(ContactCreate):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class AdminLoginRequest(BaseModel):
    email: EmailStr
    password: str

class AdminReplyRequest(BaseModel):
    message: str

# Chatbot Schemas
class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str

# Health Records Schemas
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

# Medication Schemas
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

# Appointment Schemas
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

# Symptom Checker Schema
class SymptomCheck(BaseModel):
    symptoms: str
    age: Optional[int] = None
    gender: Optional[str] = None

class SymptomCheckResponse(BaseModel):
    possible_conditions: list[str]
    recommendations: str
    severity: str  # low, medium, high

# Voice Agent Schemas
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

class VoiceSessionCreate(BaseModel):
    session_id: str
    user_id: Optional[int] = None

class VoiceSessionResponse(BaseModel):
    id: int
    session_id: str
    user_id: Optional[int]
    conversation_state: str
    collected_data: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

class AvailableSlot(BaseModel):
    doctor_name: str
    specialty: str
    date: str
    time: str
    datetime_iso: str

class VoiceAgentMessage(BaseModel):
    type: str  # "audio", "text", "slots", "confirmation", "error"
    content: Optional[str] = None
    data: Optional[dict] = None

class VoiceBookingRequest(BaseModel):
    session_id: str
    patient_name: str
    patient_age: int
    doctor_name: str
    specialty: str
    appointment_datetime: datetime
    reason: str

# Health Dashboard Schemas
class HealthProfileCreate(BaseModel):
    date_of_birth: Optional[date] = None
    biological_sex: Optional[str] = None
    blood_type: Optional[str] = None
    height: Optional[int] = None
    current_weight: Optional[int] = None

class HealthProfileResponse(HealthProfileCreate):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

class SleepRecordResponse(BaseModel):
    id: int
    user_id: int
    date: date
    sleep_start: datetime
    sleep_end: datetime
    total_duration: int
    deep_sleep: Optional[int]
    core_sleep: Optional[int]
    rem_sleep: Optional[int]
    created_at: datetime
    class Config:
        from_attributes = True

class ActivityRecordResponse(BaseModel):
    id: int
    user_id: int
    date: date
    steps: int
    distance: int
    flights_climbed: int
    active_calories: int
    basal_calories: int
    created_at: datetime
    class Config:
        from_attributes = True

class VitalRecordResponse(BaseModel):
    id: int
    user_id: int
    recorded_at: datetime
    heart_rate: Optional[int]
    oxygen_saturation: Optional[int]
    created_at: datetime
    class Config:
        from_attributes = True

class BodyMeasurementResponse(BaseModel):
    id: int
    user_id: int
    measured_at: datetime
    weight: int
    created_at: datetime
    class Config:
        from_attributes = True

class DashboardSummary(BaseModel):
    profile: Optional[HealthProfileResponse]
    today_stats: dict
    week_trends: dict
    month_averages: dict
