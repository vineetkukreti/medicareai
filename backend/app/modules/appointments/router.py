from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.modules.appointments import schemas
from app.modules.appointments.service import appointment_service
from app.modules.auth.models import User
from typing import List

router = APIRouter()

@router.post("/appointments", response_model=schemas.AppointmentResponse)
async def create_appointment(
    appointment: schemas.AppointmentCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Book a new appointment
    """
    try:
        return appointment_service.create_appointment(db, appointment, current_user, background_tasks)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/appointments", response_model=List[schemas.AppointmentResponse])
async def get_user_appointments(
    status: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all appointments for current user
    """
    return appointment_service.get_user_appointments(db, current_user.id, status)

@router.get("/appointments/{appointment_id}", response_model=schemas.AppointmentResponse)
async def get_appointment(
    appointment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific appointment
    """
    appointment = appointment_service.get_appointment_by_id(db, appointment_id, current_user.id)
    
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    return appointment

@router.put("/appointments/{appointment_id}", response_model=schemas.AppointmentResponse)
async def update_appointment(
    appointment_id: int,
    appointment: schemas.AppointmentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update an appointment
    """
    try:
        updated_appointment = appointment_service.update_appointment(db, appointment_id, appointment, current_user.id)
        if not updated_appointment:
            raise HTTPException(status_code=404, detail="Appointment not found")
        return updated_appointment
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

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
    if status not in ["scheduled", "completed", "cancelled"]:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    updated_appointment = appointment_service.update_appointment_status(db, appointment_id, status, current_user.id)
    if not updated_appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    return {"message": f"Appointment status updated to {status}"}

@router.delete("/appointments/{appointment_id}")
async def cancel_appointment(
    appointment_id: int,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cancel an appointment
    """
    success = appointment_service.cancel_appointment(db, appointment_id, current_user, background_tasks)
    
    if not success:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    return {"message": "Appointment cancelled successfully"}

@router.get("/appointments/doctors/list")
async def get_doctors_list(current_user: User = Depends(get_current_user)):
    """
    Get list of available doctors and specialties
    """
    return appointment_service.get_doctors_list()
