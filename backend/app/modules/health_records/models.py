from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Date
from sqlalchemy.sql import func
from app.core.database import Base

class HealthRecord(Base):
    __tablename__ = "health_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    record_type = Column(String)  # e.g., "lab_result", "diagnosis", "prescription"
    title = Column(String)
    description = Column(Text)
    file_url = Column(String, nullable=True)
    record_date = Column(Date)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
