from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.core.database import get_db, SessionLocal
from app.core.security import get_current_user
from app.services.rag_service import rag_service
from app.models import User, Appointment, Medication, HealthRecord, SleepRecord, ActivityRecord, HealthProfile, VitalRecord
import logging
import os
import PyPDF2
from typing import Optional

router = APIRouter()
logger = logging.getLogger(__name__)

UPLOAD_DIR = "uploads/health_records"

def extract_text_from_pdf(file_path: str) -> Optional[str]:
    """Extract text from PDF file"""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text.strip() if text.strip() else None
    except Exception as e:
        logger.error(f"Error extracting PDF text from {file_path}: {e}")
        return None

class InsightQuery(BaseModel):
    query: str

class InsightResponse(BaseModel):
    insight: str

@router.post("/query", response_model=InsightResponse)
async def get_health_insight(
    query: InsightQuery,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get personalized health insights based on authenticated user's data.
    """
    try:
        insight = rag_service.generate_insight(current_user.id, query.query)
        return {"insight": insight}
    except Exception as e:
        logger.error(f"Error generating insight for user {current_user.id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/refresh")
async def refresh_embeddings(
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Trigger a background task to refresh authenticated user's embeddings.
    """
    background_tasks.add_task(process_refresh_embeddings, current_user.id)
    return {"message": "Embedding refresh started in background"}

def process_refresh_embeddings(user_id: int):
    """
    Background task to refresh all embeddings for a user with PDF extraction
    """
    db = SessionLocal()
    try:
        logger.info(f"Starting embedding refresh for user {user_id}")
        
        # 1. Personal Info
        profile = db.query(HealthProfile).filter(HealthProfile.user_id == user_id).first()
        if profile:
            content = f"Personal Info: DOB: {profile.date_of_birth}, Sex: {profile.biological_sex}, Blood Type: {profile.blood_type}, Height: {profile.height}cm, Weight: {profile.current_weight}kg"
            rag_service.upsert_data(user_id, "personal_info", content, {"source": "health_profile"})

        # 2. Appointments
        appointments = db.query(Appointment).filter(Appointment.user_id == user_id).all()
        for appt in appointments:
            content = f"Appointment: Dr. {appt.doctor_name} ({appt.specialty}), Date: {appt.appointment_date}, Reason: {appt.reason}"
            rag_service.upsert_data(user_id, "appointment", content, {"appointment_id": appt.id})

        # 3. Medications
        medications = db.query(Medication).filter(Medication.user_id == user_id, Medication.is_active == True).all()
        for med in medications:
            content = f"Medication: {med.medication_name}, Dosage: {med.dosage}, Frequency: {med.frequency}, Start Date: {med.start_date}, Notes: {med.notes}"
            rag_service.upsert_data(user_id, "medication", content, {"medication_id": med.id})

        # 4. Health Records with PDF extraction
        records = db.query(HealthRecord).filter(HealthRecord.user_id == user_id).all()
        for record in records:
            content = f"Health Record: {record.title} ({record.record_type}), Date: {record.record_date}, Description: {record.description}"
            
            # Extract PDF content if file exists
            if record.file_url:
                filename = record.file_url.split('/')[-1]
                file_path = os.path.join(UPLOAD_DIR, filename)
                
                if os.path.exists(file_path):
                    extracted_text = extract_text_from_pdf(file_path)
                    if extracted_text:
                        content += f"\n\nExtracted File Content:\n{extracted_text}"
                        logger.info(f"Extracted {len(extracted_text)} characters from {filename}")
            
            rag_service.upsert_data(user_id, "health_record", content, {"record_id": record.id})

        # 5. Sleep Summary (Last 30 records)
        sleep_records = db.query(SleepRecord).filter(SleepRecord.user_id == user_id).order_by(SleepRecord.date.desc()).limit(30).all()
        if sleep_records:
             avg_duration = sum(s.total_duration for s in sleep_records) / len(sleep_records)
             content = f"Sleep Summary (Last 30 records): Average Duration: {avg_duration:.1f} mins. Latest: {sleep_records[0].date} - {sleep_records[0].total_duration} mins."
             rag_service.upsert_data(user_id, "sleep_summary", content, {"count": len(sleep_records)})

        # 6. Activity Summary (Last 30 records)
        activity_records = db.query(ActivityRecord).filter(ActivityRecord.user_id == user_id).order_by(ActivityRecord.date.desc()).limit(30).all()
        if activity_records:
             avg_steps = sum(a.steps for a in activity_records) / len(activity_records)
             content = f"Activity Summary (Last 30 records): Average Steps: {int(avg_steps)}. Latest: {activity_records[0].date} - {activity_records[0].steps} steps."
             rag_service.upsert_data(user_id, "activity_summary", content, {"count": len(activity_records)})

        logger.info(f"Completed embedding refresh for user {user_id}")
        
    except Exception as e:
        logger.error(f"Error refreshing embeddings: {e}")
    finally:
        db.close()
