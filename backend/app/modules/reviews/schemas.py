from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class ReviewCreate(BaseModel):
    appointment_id: int
    doctor_id: int
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5")
    comment: Optional[str] = Field(None, max_length=1000)

    @validator('rating')
    def validate_rating(cls, v):
        if v < 1 or v > 5:
            raise ValueError('Rating must be between 1 and 5')
        return v

class ReviewResponse(BaseModel):
    id: int
    patient_id: int
    patient_name: Optional[str]
    doctor_id: int
    appointment_id: int
    rating: int
    comment: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class DoctorRatingSummary(BaseModel):
    average_rating: float
    total_reviews: int
    rating_distribution: dict  # {1: count, 2: count, ...}

class ReviewExistsResponse(BaseModel):
    exists: bool
    review: Optional[ReviewResponse] = None
