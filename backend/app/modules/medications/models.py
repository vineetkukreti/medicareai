from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean, Date
from sqlalchemy.sql import func
from app.core.database import Base

class Medication(Base):
    __tablename__ = "medications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    medication_name = Column(String)
    dosage = Column(String)
    frequency = Column(String)  # e.g., "twice daily", "once daily"
    start_date = Column(Date)
    end_date = Column(Date, nullable=True)
    notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
