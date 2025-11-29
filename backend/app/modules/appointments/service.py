from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.modules.appointments.models import Appointment
from app.modules.doctors.models import Doctor
from app.modules.auth.models import User
from datetime import date, time, datetime, timedelta
from typing import List
from app.modules.appointments.schemas import TimeSlot


def generate_time_slots(start_hour: int = 9, end_hour: int = 17, interval_minutes: int = 30) -> List[dict]:
    """Generate all possible time slots for a day"""
    slots = []
    current = datetime.combine(date.today(), time(start_hour, 0))
    end = datetime.combine(date.today(), time(end_hour, 0))
    
    while current < end:
        next_time = current + timedelta(minutes=interval_minutes)
        slots.append({
            "start_time": current.time().strftime("%H:%M"),
            "end_time": next_time.time().strftime("%H:%M")
        })
        current = next_time
    
    return slots


def get_booked_slots(db: Session, doctor_id: int, appointment_date: date) -> List[str]:
    """Get all booked time slots for a doctor on a specific date"""
    appointments = db.query(Appointment).filter(
        Appointment.doctor_id == doctor_id,
        Appointment.appointment_date == appointment_date,
        Appointment.status.in_(["pending", "confirmed"])  # Exclude cancelled/completed
    ).all()
    
    booked_slots = [appt.start_time.strftime("%H:%M") for appt in appointments]
    return booked_slots


def get_available_slots(db: Session, doctor_id: int, appointment_date: date) -> List[TimeSlot]:
    """Get available time slots for a doctor on a specific date"""
    # Don't allow booking for past dates
    if appointment_date < date.today():
        return []
    
    all_slots = generate_time_slots()
    booked_slots = get_booked_slots(db, doctor_id, appointment_date)
    
    available_slots = []
    for slot in all_slots:
        is_available = slot["start_time"] not in booked_slots
        available_slots.append(TimeSlot(
            start_time=slot["start_time"],
            end_time=slot["end_time"],
            is_available=is_available
        ))
    
    return available_slots


def check_slot_availability(
    db: Session,
    doctor_id: int,
    appointment_date: date,
    start_time: time
) -> bool:
    """Check if a specific time slot is available"""
    existing = db.query(Appointment).filter(
        Appointment.doctor_id == doctor_id,
        Appointment.appointment_date == appointment_date,
        Appointment.start_time == start_time,
        Appointment.status.in_(["pending", "confirmed"])
    ).first()
    
    return existing is None


def book_appointment(
    db: Session,
    user_id: int,
    doctor_id: int,
    appointment_date: date,
    start_time: time,
    end_time: time,
    reason: str = None,
    notes: str = None
) -> Appointment:
    """Book an appointment with conflict checking"""
    # Validate doctor exists
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    if not doctor.is_available:
        raise HTTPException(status_code=400, detail="Doctor is not accepting appointments")
    
    # Check if slot is available (atomic check)
    if not check_slot_availability(db, doctor_id, appointment_date, start_time):
        raise HTTPException(status_code=409, detail="Time slot already booked")
    
    # Prevent booking past dates
    if appointment_date < date.today():
        raise HTTPException(status_code=400, detail="Cannot book appointments in the past")
    
    # Create appointment
    appointment = Appointment(
        user_id=user_id,
        doctor_id=doctor_id,
        appointment_date=appointment_date,
        start_time=start_time,
        end_time=end_time,
        reason=reason,
        notes=notes,
        status="pending"
    )
    
    db.add(appointment)
    try:
        db.commit()
        db.refresh(appointment)
    except Exception as e:
        db.rollback()
        # Handle unique constraint violation
        if "uix_doctor_date_time" in str(e):
            raise HTTPException(status_code=409, detail="Time slot was just booked by another patient")
        raise HTTPException(status_code=500, detail="Failed to book appointment")
    
    return appointment


def get_doctor_appointments(db: Session, doctor_id: int, status: str = None) -> List[Appointment]:
    """Get all appointments for a doctor"""
    query = db.query(Appointment).filter(Appointment.doctor_id == doctor_id)
    
    if status:
        query = query.filter(Appointment.status == status)
    
    return query.order_by(Appointment.appointment_date, Appointment.start_time).all()


def get_patient_appointments(db: Session, user_id: int) -> List[Appointment]:
    """Get all appointments for a patient"""
    return db.query(Appointment).filter(
        Appointment.user_id == user_id
    ).order_by(Appointment.appointment_date.desc()).all()


def update_appointment_status(db: Session, appointment_id: int, status: str, doctor_id: int = None) -> Appointment:
    """Update appointment status (for doctors)"""
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    # If doctor_id provided, verify it's their appointment
    if doctor_id and appointment.doctor_id != doctor_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this appointment")
    
    valid_statuses = ["pending", "confirmed", "completed", "cancelled"]
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {valid_statuses}")
    
    # Generate meeting link if confirming
    if status == "confirmed" and not appointment.meeting_link:
        # Generate Jitsi Meet link (Real working video call)
        import uuid
        unique_id = str(uuid.uuid4())[:8]
        # Format: https://meet.jit.si/MediCareAI-{appointment_id}-{unique_id}
        appointment.meeting_link = f"https://meet.jit.si/MediCareAI-{appointment_id}-{unique_id}"
        
        # Send confirmation email
        try:
            from app.services.email_service import email_service
            patient = db.query(User).filter(User.id == appointment.user_id).first()
            if patient:
                email_service.send_appointment_confirmation_email(
                    user_email=patient.email,
                    user_name=patient.full_name,
                    doctor_name=appointment.doctor.full_name,
                    specialty=appointment.doctor.specialty,
                    appointment_date=f"{appointment.appointment_date} at {appointment.start_time}",
                    reason=appointment.reason or "Consultation",
                    meeting_link=appointment.meeting_link
                )
        except Exception as e:
            print(f"Failed to send email: {e}")
    
    appointment.status = status
    db.commit()
    db.refresh(appointment)
    
    return appointment


def get_patient_info(db: Session, patient_id: int, doctor_id: int) -> User:
    """Get patient information (only if doctor has appointment with them)"""
    # Verify doctor has an appointment with this patient
    appointment = db.query(Appointment).filter(
        Appointment.doctor_id == doctor_id,
        Appointment.user_id == patient_id
    ).first()
    
    if not appointment:
        raise HTTPException(status_code=403, detail="No appointment with this patient")
    
    patient = db.query(User).filter(User.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    return patient
