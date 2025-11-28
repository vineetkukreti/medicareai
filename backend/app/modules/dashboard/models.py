from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date
from sqlalchemy.sql import func
from app.core.database import Base

class HealthProfile(Base):
    __tablename__ = "health_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    date_of_birth = Column(Date, nullable=True)
    biological_sex = Column(String, nullable=True)  # Male, Female, Other
    blood_type = Column(String, nullable=True)  # A+, B+, O+, AB+, etc.
    height = Column(Integer, nullable=True)  # in cm
    current_weight = Column(Integer, nullable=True)  # in kg
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class SleepRecord(Base):
    __tablename__ = "sleep_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(Date, index=True)
    sleep_start = Column(DateTime(timezone=True))
    sleep_end = Column(DateTime(timezone=True))
    total_duration = Column(Integer)  # in minutes
    deep_sleep = Column(Integer, nullable=True)  # in minutes
    core_sleep = Column(Integer, nullable=True)  # in minutes
    rem_sleep = Column(Integer, nullable=True)  # in minutes
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ActivityRecord(Base):
    __tablename__ = "activity_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(Date, index=True)
    steps = Column(Integer, default=0)
    distance = Column(Integer, default=0)  # in meters
    flights_climbed = Column(Integer, default=0)
    active_calories = Column(Integer, default=0)  # in kcal
    basal_calories = Column(Integer, default=0)  # in kcal
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class VitalRecord(Base):
    __tablename__ = "vital_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    recorded_at = Column(DateTime(timezone=True), index=True)
    heart_rate = Column(Integer, nullable=True)  # in bpm
    oxygen_saturation = Column(Integer, nullable=True)  # in percentage
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class BodyMeasurement(Base):
    __tablename__ = "body_measurements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    measured_at = Column(DateTime(timezone=True), index=True)
    weight = Column(Integer)  # in kg
    created_at = Column(DateTime(timezone=True), server_default=func.now())
