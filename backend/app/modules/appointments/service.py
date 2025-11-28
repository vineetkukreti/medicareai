from sqlalchemy.orm import Session
from app.modules.appointments import models, schemas
from app.services.email_service import email_service
from app.services.email_templates import (
    get_appointment_confirmation_email,
    get_appointment_cancellation_email,
    get_appointment_confirmation_subject,
    get_appointment_cancellation_subject
)
from app.services.rag_service import rag_service
from app.modules.auth.models import User
from datetime import datetime

class AppointmentService:
    def create_appointment(self, db: Session, appointment: schemas.AppointmentCreate, user: User, background_tasks=None):
        # Validate appointment date is in the future
        current_time = datetime.now()
        check_date = appointment.appointment_date
        
        if check_date.tzinfo is not None:
            check_date = check_date.replace(tzinfo=None)
            
        if check_date <= current_time:
            raise ValueError("Appointment date must be in the future")
        
        db_appointment = models.Appointment(**appointment.dict(), user_id=user.id)
        db.add(db_appointment)
        db.commit()
        db.refresh(db_appointment)
        
        # Send confirmation email in background
        if background_tasks:
            formatted_date = appointment.appointment_date.strftime("%B %d, %Y at %I:%M %p")
            background_tasks.add_task(
                self._send_confirmation_email,
                user=user,
                doctor_name=appointment.doctor_name,
                specialty=appointment.specialty,
                appointment_date=formatted_date,
                reason=appointment.reason
            )
            
            # Trigger RAG ingestion in background
            background_tasks.add_task(
                self._index_appointment_to_rag,
                user_id=user.id,
                appointment_id=db_appointment.id,
                doctor_name=db_appointment.doctor_name,
                specialty=db_appointment.specialty,
                appointment_date=str(db_appointment.appointment_date),
                reason=db_appointment.reason
            )
            
        return db_appointment
    
    def _send_confirmation_email(self, user, doctor_name, specialty, appointment_date, reason):
        """Background task to send appointment confirmation email"""
        try:
            email_html = get_appointment_confirmation_email(
                user_name=user.full_name or user.email.split('@')[0],
                doctor_name=doctor_name,
                specialty=specialty,
                appointment_date=appointment_date,
                reason=reason
            )
            subject = get_appointment_confirmation_subject()
            email_service.send_email(user.email, subject, email_html)
        except Exception as e:
            print(f"Failed to send confirmation email: {e}")
    
    def _index_appointment_to_rag(self, user_id, appointment_id, doctor_name, specialty, appointment_date, reason):
        """Background task to index appointment to RAG"""
        try:
            content = f"Appointment: Dr. {doctor_name} ({specialty}), Date: {appointment_date}, Reason: {reason}"
            rag_service.upsert_data(
                user_id=user_id,
                data_type="appointment",
                content=content,
                metadata={"appointment_id": appointment_id}
            )
        except Exception as e:
            print(f"Error triggering RAG ingestion: {e}")

    def get_user_appointments(self, db: Session, user_id: int, status: str = None):
        query = db.query(models.Appointment).filter(models.Appointment.user_id == user_id)
        if status:
            query = query.filter(models.Appointment.status == status)
        return query.order_by(models.Appointment.appointment_date).all()

    def get_appointment_by_id(self, db: Session, appointment_id: int, user_id: int):
        return db.query(models.Appointment).filter(
            models.Appointment.id == appointment_id,
            models.Appointment.user_id == user_id
        ).first()

    def update_appointment(self, db: Session, appointment_id: int, appointment_data: schemas.AppointmentCreate, user_id: int):
        db_appointment = self.get_appointment_by_id(db, appointment_id, user_id)
        if not db_appointment:
            return None
        
        # Validate appointment date is in the future
        current_time = datetime.now()
        check_date = appointment_data.appointment_date
        
        if check_date.tzinfo is not None:
            check_date = check_date.replace(tzinfo=None)
            
        if check_date <= current_time:
            raise ValueError("Appointment date must be in the future")
        
        for key, value in appointment_data.dict().items():
            setattr(db_appointment, key, value)
        
        db.commit()
        db.refresh(db_appointment)
        return db_appointment

    def update_appointment_status(self, db: Session, appointment_id: int, status: str, user_id: int):
        db_appointment = self.get_appointment_by_id(db, appointment_id, user_id)
        if not db_appointment:
            return None
        
        db_appointment.status = status
        db.commit()
        return db_appointment

    def cancel_appointment(self, db: Session, appointment_id: int, user: User, background_tasks=None):
        db_appointment = self.get_appointment_by_id(db, appointment_id, user.id)
        if not db_appointment:
            return False
        
        # Delete from RAG when cancelling
        try:
            rag_service.delete_by_metadata(
                user_id=user.id,
                data_type="appointment",
                metadata_key="appointment_id",
                metadata_value=appointment_id
            )
        except Exception as e:
            print(f"Error deleting from RAG: {e}")
        
        db_appointment.status = "cancelled"
        db.commit()
        
        # Send cancellation email in background
        if background_tasks:
            formatted_date = db_appointment.appointment_date.strftime("%B %d, %Y at %I:%M %p")
            background_tasks.add_task(
                self._send_cancellation_email,
                user=user,
                doctor_name=db_appointment.doctor_name,
                appointment_date=formatted_date
            )
        
        return True
    
    def _send_cancellation_email(self, user, doctor_name, appointment_date):
        """Background task to send appointment cancellation email"""
        try:
            email_html = get_appointment_cancellation_email(
                user_name=user.full_name or user.email.split('@')[0],
                doctor_name=doctor_name,
                appointment_date=appointment_date
            )
            subject = get_appointment_cancellation_subject()
            email_service.send_email(user.email, subject, email_html)
        except Exception as e:
            print(f"Failed to send cancellation email: {e}")

    def get_doctors_list(self):
        # This is a mock list - in production, this would come from a database
        doctors = [
            {"name": "Dr. Sarah Johnson", "specialty": "Cardiology"},
            {"name": "Dr. Michael Chen", "specialty": "Dermatology"},
            {"name": "Dr. Emily Rodriguez", "specialty": "Pediatrics"},
            {"name": "Dr. David Kumar", "specialty": "Orthopedics"},
            {"name": "Dr. Lisa Anderson", "specialty": "General Medicine"},
            {"name": "Dr. James Wilson", "specialty": "Neurology"},
            {"name": "Dr. Maria Garcia", "specialty": "Gynecology"},
            {"name": "Dr. Robert Taylor", "specialty": "Psychiatry"},
        ]
        
        specialties = list(set([doc["specialty"] for doc in doctors]))
        
        return {
            "doctors": doctors,
            "specialties": sorted(specialties)
        }

appointment_service = AppointmentService()
