from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

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

class SymptomCheck(BaseModel):
    symptoms: str
    age: Optional[int] = None
    gender: Optional[str] = None

class SymptomCheckResponse(BaseModel):
    possible_conditions: list[str]
    recommendations: str
    severity: str  # low, medium, high
