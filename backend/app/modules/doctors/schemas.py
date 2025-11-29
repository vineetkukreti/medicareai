from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal


class DoctorBase(BaseModel):
    email: EmailStr
    full_name: str
    specialty: str
    license_number: str
    experience_years: Optional[int] = None
    bio: Optional[str] = None
    profile_image: Optional[str] = None
    hourly_rate: Optional[Decimal] = None


class DoctorCreate(DoctorBase):
    password: str


class DoctorLogin(BaseModel):
    email: EmailStr
    password: str


class DoctorResponse(DoctorBase):
    id: int
    is_available: bool
    created_at: datetime

    class Config:
        from_attributes = True


class DoctorUpdate(BaseModel):
    full_name: Optional[str] = None
    specialty: Optional[str] = None
    experience_years: Optional[int] = None
    bio: Optional[str] = None
    profile_image: Optional[str] = None
    hourly_rate: Optional[Decimal] = None
    is_available: Optional[bool] = None


class DoctorPublic(BaseModel):
    """Public doctor info for patient browsing"""
    id: int
    full_name: str
    specialty: str
    experience_years: Optional[int]
    bio: Optional[str]
    profile_image: Optional[str]
    hourly_rate: Optional[Decimal]
    is_available: bool

    class Config:
        from_attributes = True
