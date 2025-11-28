from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import UploadFile, HTTPException, BackgroundTasks
from app.modules.dashboard import models, schemas
from app.services.health_parser import AppleHealthParser
from app.services.rag_service import rag_service
from app.services.ai_service import ai_service
from app.modules.auth.models import User
from app.modules.appointments.models import Appointment
from app.modules.medications.models import Medication
from app.modules.health_records.models import HealthRecord
import tempfile
import os
from datetime import datetime, timedelta, date
import logging
import PyPDF2
from typing import Optional

logger = logging.getLogger(__name__)

UPLOAD_DIR = "uploads/health_records"

class DashboardService:
    async def upload_health_data(self, db: Session, user_id: int, file: UploadFile):
        if not file.filename.endswith('.xml'):
            raise HTTPException(status_code=400, detail="Only XML files are supported")
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xml') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Parse the XML file
            parser = AppleHealthParser(temp_file_path)
            parser.parse()
            
            # Extract personal info
            personal_info = parser.get_personal_info()
            height, weight, weight_date = parser.get_height_weight()
            
            # Create or update health profile
            profile = db.query(models.HealthProfile).filter(models.HealthProfile.user_id == user_id).first()
            if profile:
                # Update existing profile
                for key, value in personal_info.items():
                    if value is not None:
                        setattr(profile, key, value)
                if height:
                    profile.height = height
                if weight:
                    profile.current_weight = weight
            else:
                # Create new profile
                profile = models.HealthProfile(
                    user_id=user_id,
                    height=height,
                    current_weight=weight,
                    **personal_info
                )
                db.add(profile)
            
            # Extract and save sleep records
            sleep_records = parser.get_sleep_records()
            sleep_count = 0
            for sleep_data in sleep_records:
                # Check if record already exists
                existing = db.query(models.SleepRecord).filter(
                    models.SleepRecord.user_id == user_id,
                    models.SleepRecord.date == sleep_data['date']
                ).first()
                
                if not existing:
                    sleep_record = models.SleepRecord(user_id=user_id, **sleep_data)
                    db.add(sleep_record)
                    sleep_count += 1
            
            # Extract and save activity records
            activity_records = parser.get_activity_records()
            activity_count = 0
            for activity_data in activity_records:
                # Check if record already exists
                existing = db.query(models.ActivityRecord).filter(
                    models.ActivityRecord.user_id == user_id,
                    models.ActivityRecord.date == activity_data['date']
                ).first()
                
                if existing:
                    # Update existing record
                    for key, value in activity_data.items():
                        if key != 'date':
                            setattr(existing, key, value)
                else:
                    activity_record = models.ActivityRecord(user_id=user_id, **activity_data)
                    db.add(activity_record)
                    activity_count += 1
            
            # Extract and save vital records
            vital_records = parser.get_vital_records()
            vital_count = 0
            for vital_data in vital_records:
                # Only save if we don't have a record within 1 minute
                existing = db.query(models.VitalRecord).filter(
                    models.VitalRecord.user_id == user_id,
                    models.VitalRecord.recorded_at >= vital_data['recorded_at'] - timedelta(minutes=1),
                    models.VitalRecord.recorded_at <= vital_data['recorded_at'] + timedelta(minutes=1)
                ).first()
                
                if not existing:
                    vital_record = models.VitalRecord(user_id=user_id, **vital_data)
                    db.add(vital_record)
                    vital_count += 1
            
            # Save weight measurement if available
            if weight and weight_date:
                existing_weight = db.query(models.BodyMeasurement).filter(
                    models.BodyMeasurement.user_id == user_id,
                    models.BodyMeasurement.measured_at == weight_date
                ).first()
                
                if not existing_weight:
                    weight_record = models.BodyMeasurement(
                        user_id=user_id,
                        measured_at=weight_date,
                        weight=weight
                    )
                    db.add(weight_record)
            
            db.commit()
            
            # Trigger RAG ingestion in background
            try:
                # Upsert personal info
                rag_service.upsert_data(
                    user_id=user_id,
                    data_type="personal_info",
                    content=f"Personal Info: {personal_info}, Height: {height}cm, Weight: {weight}kg",
                    metadata={"source": "apple_health_export"}
                )
                
                # Upsert sleep summary
                if sleep_records:
                    sleep_summary = f"Recent sleep records: {len(sleep_records)} records found. Last record: {sleep_records[-1]['date']} - {sleep_records[-1]['total_duration']} mins"
                    rag_service.upsert_data(
                        user_id=user_id,
                        data_type="sleep_records",
                        content=sleep_summary,
                        metadata={"count": len(sleep_records), "last_date": str(sleep_records[-1]['date'])}
                    )
                    
                # Upsert activity summary
                if activity_records:
                    activity_summary = f"Recent activity records: {len(activity_records)} records found. Last record: {activity_records[-1]['date']} - Steps: {activity_records[-1].get('steps', 0)}"
                    rag_service.upsert_data(
                        user_id=user_id,
                        data_type="activity_records",
                        content=activity_summary,
                        metadata={"count": len(activity_records), "last_date": str(activity_records[-1]['date'])}
                    )
                    
            except Exception as e:
                print(f"Error triggering RAG ingestion: {e}")
            
            return {
                "message": "Health data uploaded successfully",
                "summary": {
                    "sleep_records": sleep_count,
                    "activity_records": activity_count,
                    "vital_records": vital_count,
                    "profile_updated": True
                }
            }
            
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error parsing health data: {str(e)}")
        finally:
            # Clean up temp file
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

    def get_health_profile(self, db: Session, user_id: int):
        return db.query(models.HealthProfile).filter(models.HealthProfile.user_id == user_id).first()

    def get_sleep_records(self, db: Session, user_id: int, start_date: Optional[date] = None, end_date: Optional[date] = None):
        query = db.query(models.SleepRecord).filter(models.SleepRecord.user_id == user_id)
        if start_date:
            query = query.filter(models.SleepRecord.date >= start_date)
        if end_date:
            query = query.filter(models.SleepRecord.date <= end_date)
        return query.order_by(models.SleepRecord.date.desc()).all()

    def get_activity_records(self, db: Session, user_id: int, start_date: Optional[date] = None, end_date: Optional[date] = None):
        query = db.query(models.ActivityRecord).filter(models.ActivityRecord.user_id == user_id)
        if start_date:
            query = query.filter(models.ActivityRecord.date >= start_date)
        if end_date:
            query = query.filter(models.ActivityRecord.date <= end_date)
        return query.order_by(models.ActivityRecord.date.desc()).all()

    def get_vital_records(self, db: Session, user_id: int, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None, limit: int = 100):
        query = db.query(models.VitalRecord).filter(models.VitalRecord.user_id == user_id)
        if start_date:
            query = query.filter(models.VitalRecord.recorded_at >= start_date)
        if end_date:
            query = query.filter(models.VitalRecord.recorded_at <= end_date)
        return query.order_by(models.VitalRecord.recorded_at.desc()).limit(limit).all()

    def get_dashboard_summary(self, db: Session, user_id: int):
        profile = self.get_health_profile(db, user_id)
        
        today = date.today()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        
        # Today's stats
        today_activity = db.query(models.ActivityRecord).filter(
            models.ActivityRecord.user_id == user_id,
            models.ActivityRecord.date == today
        ).first()
        
        last_night_sleep = db.query(models.SleepRecord).filter(
            models.SleepRecord.user_id == user_id,
            models.SleepRecord.date == today
        ).first()
        
        latest_heart_rate = db.query(models.VitalRecord).filter(
            models.VitalRecord.user_id == user_id,
            models.VitalRecord.heart_rate.isnot(None)
        ).order_by(models.VitalRecord.recorded_at.desc()).first()
        
        today_stats = {
            "steps": today_activity.steps if today_activity else 0,
            "active_calories": today_activity.active_calories if today_activity else 0,
            "distance": today_activity.distance if today_activity else 0,
            "sleep_duration": last_night_sleep.total_duration if last_night_sleep else 0,
            "heart_rate": latest_heart_rate.heart_rate if latest_heart_rate else None
        }
        
        # Week trends (last 7 days)
        week_activities = db.query(models.ActivityRecord).filter(
            models.ActivityRecord.user_id == user_id,
            models.ActivityRecord.date >= week_ago,
            models.ActivityRecord.date <= today
        ).all()
        
        week_sleep = db.query(models.SleepRecord).filter(
            models.SleepRecord.user_id == user_id,
            models.SleepRecord.date >= week_ago,
            models.SleepRecord.date <= today
        ).all()
        
        week_trends = {
            "daily_steps": [{"date": str(a.date), "steps": a.steps} for a in week_activities],
            "daily_sleep": [{"date": str(s.date), "duration": s.total_duration} for s in week_sleep],
            "total_steps": sum(a.steps for a in week_activities),
            "avg_sleep": sum(s.total_duration for s in week_sleep) / len(week_sleep) if week_sleep else 0
        }
        
        # Month averages (last 30 days)
        month_activities = db.query(models.ActivityRecord).filter(
            models.ActivityRecord.user_id == user_id,
            models.ActivityRecord.date >= month_ago,
            models.ActivityRecord.date <= today
        ).all()
        
        month_sleep = db.query(models.SleepRecord).filter(
            models.SleepRecord.user_id == user_id,
            models.SleepRecord.date >= month_ago,
            models.SleepRecord.date <= today
        ).all()
        
        month_heart_rate = db.query(func.avg(models.VitalRecord.heart_rate)).filter(
            models.VitalRecord.user_id == user_id,
            models.VitalRecord.recorded_at >= datetime.combine(month_ago, datetime.min.time()),
            models.VitalRecord.heart_rate.isnot(None)
        ).scalar()
        
        month_averages = {
            "avg_steps": int(sum(a.steps for a in month_activities) / len(month_activities)) if month_activities else 0,
            "avg_sleep": int(sum(s.total_duration for s in month_sleep) / len(month_sleep)) if month_sleep else 0,
            "avg_heart_rate": int(month_heart_rate) if month_heart_rate else None,
            "total_distance": sum(a.distance for a in month_activities)
        }
        
        return schemas.DashboardSummary(
            profile=schemas.HealthProfileResponse.from_orm(profile) if profile else None,
            today_stats=today_stats,
            week_trends=week_trends,
            month_averages=month_averages
        )

    async def analyze_symptoms(self, symptoms: str, age: Optional[int], gender: Optional[str]):
        return await ai_service.analyze_symptoms(symptoms=symptoms, age=age, gender=gender)

    async def get_health_advice(self, topic: str):
        return await ai_service.get_health_advice(topic)

    def generate_insight(self, user_id: int, query: str):
        return rag_service.generate_insight(user_id, query)

    def extract_text_from_pdf(self, file_path: str) -> Optional[str]:
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

    def process_refresh_embeddings(self, user_id: int, db: Session):
        try:
            logger.info(f"Starting embedding refresh for user {user_id}")
            
            # 1. Personal Info
            profile = db.query(models.HealthProfile).filter(models.HealthProfile.user_id == user_id).first()
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
                        extracted_text = self.extract_text_from_pdf(file_path)
                        if extracted_text:
                            content += f"\n\nExtracted File Content:\n{extracted_text}"
                            logger.info(f"Extracted {len(extracted_text)} characters from {filename}")
                
                rag_service.upsert_data(user_id, "health_record", content, {"record_id": record.id})

            # 5. Sleep Summary (Last 30 records)
            sleep_records = db.query(models.SleepRecord).filter(models.SleepRecord.user_id == user_id).order_by(models.SleepRecord.date.desc()).limit(30).all()
            if sleep_records:
                 avg_duration = sum(s.total_duration for s in sleep_records) / len(sleep_records)
                 content = f"Sleep Summary (Last 30 records): Average Duration: {avg_duration:.1f} mins. Latest: {sleep_records[0].date} - {sleep_records[0].total_duration} mins."
                 rag_service.upsert_data(user_id, "sleep_summary", content, {"count": len(sleep_records)})

            # 6. Activity Summary (Last 30 records)
            activity_records = db.query(models.ActivityRecord).filter(models.ActivityRecord.user_id == user_id).order_by(models.ActivityRecord.date.desc()).limit(30).all()
            if activity_records:
                 avg_steps = sum(a.steps for a in activity_records) / len(activity_records)
                 content = f"Activity Summary (Last 30 records): Average Steps: {int(avg_steps)}. Latest: {activity_records[0].date} - {activity_records[0].steps} steps."
                 rag_service.upsert_data(user_id, "activity_summary", content, {"count": len(activity_records)})

            logger.info(f"Completed embedding refresh for user {user_id}")
            
        except Exception as e:
            logger.error(f"Error refreshing embeddings: {e}")

dashboard_service = DashboardService()
