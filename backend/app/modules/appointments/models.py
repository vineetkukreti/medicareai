from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.sql import func
from app.core.database import Base

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    doctor_name = Column(String)
    specialty = Column(String)
    appointment_date = Column(DateTime(timezone=True))
    reason = Column(Text)
    status = Column(String, default="scheduled")  # scheduled, completed, cancelled
    notes = Column(Text, nullable=True)
    created_via = Column(String, default="web")  # web, voice
    created_at = Column(DateTime(timezone=True), server_default=func.now())

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
