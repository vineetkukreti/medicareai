from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.modules.auth.models import User
from app.modules.doctors.models import Doctor
from app.modules.appointments.models import Appointment
from app.modules.admin import schemas

class AdminService:
    def get_stats(self, db: Session) -> schemas.StatsResponse:
        total_patients = db.query(func.count(User.id)).scalar()
        total_doctors = db.query(func.count(Doctor.id)).scalar()
        total_appointments = db.query(func.count(Appointment.id)).scalar()
        
        # Calculate revenue (simplified: sum of doctor hourly rates for completed appointments)
        # This is an approximation as appointment duration varies
        revenue = db.query(func.sum(Doctor.hourly_rate))\
            .join(Appointment, Doctor.id == Appointment.doctor_id)\
            .filter(Appointment.status == "completed")\
            .scalar() or 0.0
            
        # Pending doctors (assuming we will add is_verified later, for now using a placeholder logic or checking if we can add the field)
        # For now, let's assume all doctors are verified or use a mocked field if not present
        # We will return 0 for pending if field doesn't exist
        pending_doctors = 0 
        
        active_patients = total_patients # Placeholder
        
        return schemas.StatsResponse(
            total_patients=total_patients,
            total_doctors=total_doctors,
            total_appointments=total_appointments,
            total_revenue=float(revenue),
            pending_doctors=pending_doctors,
            active_patients=active_patients
        )

    def get_patients(self, db: Session, skip: int = 0, limit: int = 100) -> List[schemas.PatientSummary]:
        users = db.query(User).offset(skip).limit(limit).all()
        return [
            schemas.PatientSummary(
                id=u.id,
                full_name=u.full_name,
                email=u.email,
                created_at=u.created_at,
                is_active=True # Default
            ) for u in users
        ]

    def get_doctors(self, db: Session, skip: int = 0, limit: int = 100) -> List[schemas.DoctorSummary]:
        doctors = db.query(Doctor).offset(skip).limit(limit).all()
        return [
            schemas.DoctorSummary(
                id=d.id,
                full_name=d.full_name,
                email=d.email,
                specialization=d.specialty,
                experience_years=d.experience_years or 0,
                is_verified=True, # Default until field added
                rating=4.5, # Placeholder
                consultation_fee=float(d.hourly_rate or 0),
                created_at=d.created_at
            ) for d in doctors
        ]

admin_service = AdminService()
