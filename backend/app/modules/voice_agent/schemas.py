from pydantic import BaseModel
from typing import Optional
from datetime import datetime

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
