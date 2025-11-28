from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean, Date
from sqlalchemy.sql import func
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    phone_number = Column(String, nullable=True)
    date_of_birth = Column(Date, nullable=True)
    gender = Column(String, nullable=True)
    address = Column(Text, nullable=True)
    emergency_contact_name = Column(String, nullable=True)
    emergency_contact_phone = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ContactMessage(Base):
    __tablename__ = "contact_messages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    message = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ChatConversation(Base):
    __tablename__ = "chat_conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    session_id = Column(String, index=True)
    user_message = Column(Text)
    bot_response = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

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

class VoiceSession(Base):
    __tablename__ = "voice_sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    conversation_state = Column(String, default="greeting")  # greeting, collecting_name, collecting_age, etc.
    collected_data = Column(Text, nullable=True)  # JSON string storing collected information
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

# Health Dashboard Models
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
