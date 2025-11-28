from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas import AppointmentCreate, AppointmentResponse
from app.models import Appointment, User
from app.services.email_service import email_service
from app.services.email_templates import (
    get_appointment_confirmation_email,
    get_appointment_cancellation_email,
    get_appointment_confirmation_subject,
    get_appointment_cancellation_subject
)
from typing import List
from datetime import datetime
from app.services.rag_service import rag_service

router = APIRouter()

@router.post("/appointments", response_model=AppointmentResponse)
async def create_appointment(
    appointment: AppointmentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Book a new appointment
    """
    # Validate appointment date is in the future
    # Validate appointment date is in the future
    # Convert both to naive UTC or ensure both are aware. 
    # Simplest fix: make appointment_date naive if it's aware, or make now() aware.
    # Since we want to compare with local time or UTC, let's standardize.
    
    # If appointment_date has timezone info, convert to naive (UTC) for comparison or make now() aware
    current_time = datetime.now()
    check_date = appointment.appointment_date
    
    if check_date.tzinfo is not None:
        check_date = check_date.replace(tzinfo=None)
        
    if check_date <= current_time:
        raise HTTPException(
            status_code=400,
            detail="Appointment date must be in the future"
        )
    
    db_appointment = Appointment(**appointment.dict(), user_id=current_user.id)
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    
    # Send confirmation email
    try:
        formatted_date = appointment.appointment_date.strftime("%B %d, %Y at %I:%M %p")
        email_html = get_appointment_confirmation_email(
            user_name=current_user.full_name or current_user.email.split('@')[0],
            doctor_name=appointment.doctor_name,
            specialty=appointment.specialty,
            appointment_date=formatted_date,
            reason=appointment.reason
        )
        subject = get_appointment_confirmation_subject()
        email_service.send_email(current_user.email, subject, email_html)
    except Exception as e:
        # Log error but don't fail the appointment creation
        print(f"Failed to send confirmation email: {e}")
    
    # Trigger RAG ingestion
    try:
        content = f"Appointment: Dr. {db_appointment.doctor_name} ({db_appointment.specialty}), Date: {db_appointment.appointment_date}, Reason: {db_appointment.reason}"
        rag_service.upsert_data(
            user_id=current_user.id,
            data_type="appointment",
            content=content,
            metadata={"appointment_id": db_appointment.id}
        )
    except Exception as e:
        print(f"Error triggering RAG ingestion: {e}")

    return db_appointment

@router.get("/appointments", response_model=List[AppointmentResponse])
async def get_user_appointments(
    status: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all appointments for current user
    """
    query = db.query(Appointment).filter(Appointment.user_id == current_user.id)
    if status:
        query = query.filter(Appointment.status == status)
    appointments = query.order_by(Appointment.appointment_date).all()
    return appointments

@router.get("/appointments/{appointment_id}", response_model=AppointmentResponse)
async def get_appointment(
    appointment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific appointment
    """
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id,
        Appointment.user_id == current_user.id
    ).first()
    
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    return appointment

@router.put("/appointments/{appointment_id}", response_model=AppointmentResponse)
async def update_appointment(
    appointment_id: int,
    appointment: AppointmentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update an appointment
    """
    db_appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id,
        Appointment.user_id == current_user.id
    ).first()
    
    if not db_appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    # Validate appointment date is in the future
    # Validate appointment date is in the future
    current_time = datetime.now()
    check_date = appointment.appointment_date
    
    if check_date.tzinfo is not None:
        check_date = check_date.replace(tzinfo=None)
        
    if check_date <= current_time:
        raise HTTPException(
            status_code=400,
            detail="Appointment date must be in the future"
        )
    
    for key, value in appointment.dict().items():
        setattr(db_appointment, key, value)
    
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

@router.patch("/appointments/{appointment_id}/status")
async def update_appointment_status(
    appointment_id: int,
    status: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update appointment status (scheduled, completed, cancelled)
    """
    db_appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id,
        Appointment.user_id == current_user.id
    ).first()
    
    if not db_appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    if status not in ["scheduled", "completed", "cancelled"]:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    db_appointment.status = status
    db.commit()
    return {"message": f"Appointment status updated to {status}"}

@router.delete("/appointments/{appointment_id}")
async def cancel_appointment(
    appointment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cancel an appointment
    """
    db_appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id,
        Appointment.user_id == current_user.id
    ).first()
    
    if not db_appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    db_appointment.status = "cancelled"
    db.commit()
    
    # Send cancellation email
    try:
        formatted_date = db_appointment.appointment_date.strftime("%B %d, %Y at %I:%M %p")
        email_html = get_appointment_cancellation_email(
            user_name=current_user.full_name or current_user.email.split('@')[0],
            doctor_name=db_appointment.doctor_name,
            appointment_date=formatted_date
        )
        subject = get_appointment_cancellation_subject()
        email_service.send_email(current_user.email, subject, email_html)
    except Exception as e:
        print(f"Failed to send cancellation email: {e}")
    
    return {"message": "Appointment cancelled successfully"}

@router.get("/appointments/doctors/list")
async def get_doctors_list(current_user: User = Depends(get_current_user)):
    """
    Get list of available doctors and specialties
    """
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
