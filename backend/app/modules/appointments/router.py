from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user, get_current_doctor
from app.modules.appointments import schemas
from app.modules.appointments.models import Appointment
from app.modules.appointments import service
from app.modules.doctors.models import Doctor
from app.modules.auth.models import User
from typing import List
from datetime import date, time as time_type

router = APIRouter()


# ===== PATIENT ENDPOINTS =====

@router.get("/doctors/{doctor_id}/availability", response_model=List[schemas.TimeSlot])
def get_doctor_availability(
    doctor_id: int,
    appointment_date: date,
    db: Session = Depends(get_db)
):
    """Get available time slots for a doctor on a specific date"""
    return service.get_available_slots(db, doctor_id, appointment_date)


@router.post("/book", response_model=schemas.AppointmentResponse, status_code=status.HTTP_201_CREATED)
def book_appointment(
    appointment_data: schemas.AppointmentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Book an appointment (patient endpoint)"""
    # Use current_user directly
    user = current_user
    
    appointment = service.book_appointment(
        db=db,
        user_id=user.id,
        doctor_id=appointment_data.doctor_id,
        appointment_date=appointment_data.appointment_date,
        start_time=appointment_data.start_time,
        end_time=appointment_data.end_time,
        reason=appointment_data.reason,
        notes=appointment_data.notes
    )
    
    # Add doctor and patient names to response
    appointment.doctor_name = appointment.doctor.full_name if appointment.doctor else None
    appointment.patient_name = user.full_name
    
    return appointment


@router.get("/my-appointments", response_model=List[schemas.AppointmentResponse])
def get_my_appointments(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all appointments for current patient"""
    user = current_user
    
    appointments = service.get_patient_appointments(db, user.id)
    
    # Add doctor names
    for appt in appointments:
        appt.doctor_name = appt.doctor.full_name if appt.doctor else appt.doctor_name
        appt.patient_name = user.full_name
    
    return appointments


@router.delete("/{appointment_id}")
def cancel_appointment(
    appointment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cancel an appointment (patient endpoint)"""
    user = current_user
    
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id,
        Appointment.user_id == user.id
    ).first()
    
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    appointment.status = "cancelled"
    db.commit()
    
    return {"message": "Appointment cancelled successfully"}


# ===== DOCTOR ENDPOINTS =====

@router.get("/doctor/my-appointments", response_model=List[schemas.AppointmentResponse])
def get_doctor_appointments(
    status_filter: str = None,
    current_doctor: Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    """Get all appointments for current doctor"""
    appointments = service.get_doctor_appointments(db, current_doctor.id, status_filter)
    
    # Add patient names
    for appt in appointments:
        appt.doctor_name = current_doctor.full_name
        appt.patient_name = appt.patient.full_name if appt.patient else None
    
    return appointments


@router.put("/doctor/appointments/{appointment_id}", response_model=schemas.AppointmentResponse)
def update_appointment(
    appointment_id: int,
    update_data: schemas.AppointmentUpdate,
    current_doctor: Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    """Update appointment status (doctor endpoint)"""
    appointment = service.update_appointment_status(
        db, appointment_id, update_data.status, current_doctor.id
    )
    
    # Update notes if provided
    if update_data.notes:
        appointment.notes = update_data.notes
        db.commit()
        db.refresh(appointment)
    
    appointment.doctor_name = current_doctor.full_name
    appointment.patient_name = appointment.patient.full_name if appointment.patient else None
    
    return appointment


@router.get("/doctor/patients/{patient_id}", response_model=schemas.PatientInfo)
def get_patient_details(
    patient_id: int,
    current_doctor: Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    """Get patient information (only if doctor has appointment with them)"""
    patient = service.get_patient_info(db, patient_id, current_doctor.id)
    
    return patient
