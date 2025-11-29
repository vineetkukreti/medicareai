from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_password_hash, verify_password, create_access_token, get_current_user, get_current_doctor
from app.modules.doctors.models import Doctor
from app.modules.doctors.schemas import DoctorCreate, DoctorLogin, DoctorResponse, DoctorUpdate, DoctorPublic
from app.modules.auth.models import User
from typing import List

router = APIRouter()


@router.post("/register", response_model=DoctorResponse, status_code=status.HTTP_201_CREATED)
def register_doctor(doctor: DoctorCreate, db: Session = Depends(get_db)):
    """Register a new doctor"""
    # Check if email already exists
    existing_doctor = db.query(Doctor).filter(Doctor.email == doctor.email).first()
    if existing_doctor:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Check if license number already exists
    existing_license = db.query(Doctor).filter(Doctor.license_number == doctor.license_number).first()
    if existing_license:
        raise HTTPException(status_code=400, detail="License number already registered")
    
    # Create new doctor
    hashed_password = get_password_hash(doctor.password)
    db_doctor = Doctor(
        email=doctor.email,
        password_hash=hashed_password,
        full_name=doctor.full_name,
        specialty=doctor.specialty,
        license_number=doctor.license_number,
        experience_years=doctor.experience_years,
        bio=doctor.bio,
        profile_image=doctor.profile_image,
        hourly_rate=doctor.hourly_rate
    )
    
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor


@router.post("/login")
def login_doctor(credentials: DoctorLogin, db: Session = Depends(get_db)):
    """Doctor login"""
    doctor = db.query(Doctor).filter(Doctor.email == credentials.email).first()
    
    if not doctor or not verify_password(credentials.password, doctor.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Create access token with doctor role
    access_token = create_access_token(data={"sub": doctor.email, "role": "doctor", "doctor_id": doctor.id})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "doctor_id": doctor.id,
        "full_name": doctor.full_name,
        "email": doctor.email,
        "specialty": doctor.specialty
    }


@router.get("/profile", response_model=DoctorResponse)
def get_doctor_profile(current_doctor: Doctor = Depends(get_current_doctor)):
    """Get current doctor's profile"""
    return current_doctor
    
    doctor = db.query(Doctor).filter(Doctor.email == current_user["sub"]).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    return doctor


@router.put("/profile", response_model=DoctorResponse)
def update_doctor_profile(
    updates: DoctorUpdate,
    current_doctor: Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    """Update doctor profile"""
    doctor = current_doctor
    
    # Update fields
    update_data = updates.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(doctor, field, value)
    
    db.commit()
    db.refresh(doctor)
    return doctor


@router.get("/list", response_model=List[DoctorPublic])
def list_doctors(
    specialty: str = None,
    available_only: bool = True,
    db: Session = Depends(get_db)
):
    """List all doctors (for patients to browse)"""
    query = db.query(Doctor)
    
    if available_only:
        query = query.filter(Doctor.is_available == True)
    
    if specialty:
        query = query.filter(Doctor.specialty == specialty)
    
    doctors = query.all()
    return doctors


@router.get("/{doctor_id}", response_model=DoctorPublic)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    """Get doctor details by ID"""
    return doctor


from fastapi import UploadFile, File
import shutil
import os
import uuid

@router.post("/upload-image")
async def upload_doctor_image(
    file: UploadFile = File(...),
    current_doctor: Doctor = Depends(get_current_doctor)
):
    """Upload doctor profile image"""
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Create upload dir if not exists
    UPLOAD_DIR = "static/uploads/doctors"
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    # Generate unique filename
    ext = file.filename.split(".")[-1]
    filename = f"{current_doctor.id}_{uuid.uuid4()}.{ext}"
    file_path = f"{UPLOAD_DIR}/{filename}"
    
    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Return URL
    # In production, this should be a full URL or CDN link
    # For local dev, we return the relative path served by StaticFiles
    return {"url": f"http://localhost:8000/{file_path}"}


# ===== PATIENT HEALTH DATA ACCESS =====

from app.modules.health_records import schemas as hr_schemas
from app.modules.medications import schemas as med_schemas
from app.modules.health_records.service import health_record_service
from app.modules.medications.service import medication_service
from app.modules.appointments.models import Appointment
from app.modules.chat.schemas import ChatMessage
from app.services.rag_service import rag_service

def verify_doctor_patient_relationship(db: Session, doctor_id: int, patient_id: int):
    """Verify that the doctor has an appointment with the patient"""
    appointment = db.query(Appointment).filter(
        Appointment.doctor_id == doctor_id,
        Appointment.user_id == patient_id
    ).first()
    
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. You can only view data for patients with booked appointments."
        )
    return True

@router.get("/patients/{patient_id}/health-records", response_model=List[hr_schemas.HealthRecordResponse])
def get_patient_health_records(
    patient_id: int,
    current_doctor: Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    """Get health records for a specific patient (Doctor only)"""
    verify_doctor_patient_relationship(db, current_doctor.id, patient_id)
    return health_record_service.get_user_health_records(db, patient_id)

@router.get("/patients/{patient_id}/medications", response_model=List[med_schemas.MedicationResponse])
def get_patient_medications(
    patient_id: int,
    current_doctor: Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    """Get medications for a specific patient (Doctor only)"""
    verify_doctor_patient_relationship(db, current_doctor.id, patient_id)
    return medication_service.get_user_medications(db, patient_id, active_only=False)

from fastapi.responses import FileResponse
from app.modules.health_records.service import UPLOAD_DIR
import mimetypes

@router.get("/patients/{patient_id}/health-records/download/{filename}")
async def download_patient_health_record(
    patient_id: int,
    filename: str,
    db: Session = Depends(get_db),
    current_doctor: Doctor = Depends(get_current_doctor)
):
    """
    Download a patient's health record file.
    Verifies doctor-patient relationship and file ownership.
    """
    # Verify relationship
    verify_doctor_patient_relationship(db, current_doctor.id, patient_id)
    
    # Verify file belongs to patient
    if not filename.startswith(f"{patient_id}_"):
        raise HTTPException(status_code=403, detail="File does not belong to this patient")
        
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
        
    # Guess media type
    media_type, _ = mimetypes.guess_type(file_path)
    if media_type is None:
        media_type = "application/octet-stream"
        
    return FileResponse(file_path, media_type=media_type, filename=filename)

@router.post("/patients/{patient_id}/chat")
async def chat_about_patient(
    patient_id: int,
    chat_message: ChatMessage,
    db: Session = Depends(get_db),
    current_doctor: Doctor = Depends(get_current_doctor)
):
    """
    Doctor chats with AI about a specific patient's data.
    """
    # Verify relationship
    verify_doctor_patient_relationship(db, current_doctor.id, patient_id)
    
    # Get AI response using RAG
    response = rag_service.answer_doctor_query(patient_id, chat_message.message)
    
    return {"response": response}
