from sqlalchemy import Column, Integer, String, Boolean, Text, DECIMAL, DateTime, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    specialty = Column(String(100), nullable=False)
    license_number = Column(String(50), unique=True, nullable=False)
    experience_years = Column(Integer)
    bio = Column(Text)
    profile_image = Column(String(500))
    hourly_rate = Column(DECIMAL(10, 2))
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    appointments = relationship("Appointment", back_populates="doctor", cascade="all, delete-orphan")

    class Config:
        from_attributes = True
