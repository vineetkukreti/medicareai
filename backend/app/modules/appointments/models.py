from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean, Date, Time, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id", ondelete="CASCADE"), nullable=True)  # Nullable for backward compatibility
    
    # Legacy fields (for old appointments without doctor_id)
    doctor_name = Column(String, nullable=True)
    specialty = Column(String, nullable=True)
    
    # New time slot fields
    appointment_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    
    reason = Column(Text)
    status = Column(String, default="pending")  # pending, confirmed, completed, cancelled
    notes = Column(Text, nullable=True)
    meeting_link = Column(String, nullable=True)  # URL for the video call
    created_via = Column(String, default="web")  # web, voice
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    doctor = relationship("Doctor", back_populates="appointments")
    patient = relationship("User", back_populates="appointments")

    # Prevent double-booking: unique constraint on doctor, date, and start_time
    __table_args__ = (
        UniqueConstraint('doctor_id', 'appointment_date', 'start_time', name='uix_doctor_date_time'),
    )

    class Config:
        from_attributes = True


class DoctorSchedule(Base):
    __tablename__ = "doctor_schedules"

    id = Column(Integer, primary_key=True, index=True)
    doctor_name = Column(String)
    specialty = Column(String)
    day_of_week = Column(Integer)  # 0=Monday, 6=Sunday
    start_time = Column(String)  # Format: "09:00"
    end_time = Column(String)  # Format: "17:00"
    slot_duration = Column(Integer, default=30)  # Duration in minutes
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
