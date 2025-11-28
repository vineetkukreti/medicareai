from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.modules.health_records import schemas
from app.modules.health_records.service import health_record_service, UPLOAD_DIR
from app.modules.auth.models import User
from typing import List
import os
import mimetypes

router = APIRouter()

@router.post("/health-records/upload")
async def upload_health_record_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """
    Upload a health record file (PDF, images, documents)
    """
    return await health_record_service.upload_file(file, current_user.id)

@router.get("/health-records/download/{filename}")
async def download_health_record_file(
    filename: str,
    current_user: User = Depends(get_current_user)
):
    """
    Download a health record file
    """
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    # Check if file exists
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    # Verify file belongs to current user (filename starts with user_id)
    if not filename.startswith(f"{current_user.id}_"):
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Get MIME type
    mime_type, _ = mimetypes.guess_type(file_path)
    
    return FileResponse(
        file_path,
        media_type=mime_type,
        filename=filename.split('_', 2)[-1]  # Return original filename
    )

@router.post("/health-records", response_model=schemas.HealthRecordResponse)
async def create_health_record(
    record: schemas.HealthRecordCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new health record with automatic text extraction from uploaded files
    """
    return health_record_service.create_health_record(db, record, current_user.id)

@router.get("/health-records", response_model=List[schemas.HealthRecordResponse])
async def get_user_health_records(
    record_type: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all health records for current user
    """
    return health_record_service.get_user_health_records(db, current_user.id, record_type)

@router.get("/health-records/detail/{record_id}", response_model=schemas.HealthRecordResponse)
async def get_health_record(
    record_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific health record
    """
    record = health_record_service.get_health_record_by_id(db, record_id, current_user.id)
    
    if not record:
        raise HTTPException(status_code=404, detail="Health record not found")
    return record

@router.delete("/health-records/{record_id}")
async def delete_health_record(
    record_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a health record
    """
    success = health_record_service.delete_health_record(db, record_id, current_user.id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Health record not found")
    
    return {"message": "Health record deleted successfully"}
