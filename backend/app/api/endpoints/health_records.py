from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas import HealthRecordCreate, HealthRecordResponse
from app.models import HealthRecord, User
from typing import List, Optional
import os
import shutil
from datetime import datetime
import mimetypes
from app.services.rag_service import rag_service
import PyPDF2
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# Allowed file types and max size
ALLOWED_EXTENSIONS = {'.pdf', '.jpg', '.jpeg', '.png', '.docx', '.doc'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

UPLOAD_DIR = "uploads/health_records"

def extract_text_from_file(file_path: str) -> Optional[str]:
    """
    Extract text content from uploaded files (PDF, images, docs)
    """
    try:
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == '.pdf':
            # Extract text from PDF
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text.strip() if text.strip() else None
        
        # TODO: Add support for .docx and image OCR in the future
        # elif file_ext in ['.docx', '.doc']:
        #     # Extract text from Word documents
        #     pass
        # elif file_ext in ['.jpg', '.jpeg', '.png']:
        #     # Use OCR to extract text from images
        #     pass
        
        return None
    except Exception as e:
        logger.error(f"Error extracting text from {file_path}: {e}")
        return None

@router.post("/health-records/upload")
async def upload_health_record_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """
    Upload a health record file (PDF, images, documents)
    """
    # Validate file extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Read file content to check size
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: 10MB"
        )
    
    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_filename = f"{current_user.id}_{timestamp}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, safe_filename)
    
    # Save file
    with open(file_path, "wb") as f:
        f.write(content)
    
    # Return file URL
    file_url = f"/health-records/download/{safe_filename}"
    
    return {
        "success": True,
        "file_url": file_url,
        "filename": file.filename,
        "size": len(content)
    }

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

@router.post("/health-records", response_model=HealthRecordResponse)
async def create_health_record(
    record: HealthRecordCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new health record with automatic text extraction from uploaded files
    """
    db_record = HealthRecord(**record.dict(), user_id=current_user.id)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    
    # Trigger RAG ingestion with file content extraction
    try:
        # Start with basic record info
        content = f"Health Record: {db_record.title} ({db_record.record_type}), Date: {db_record.record_date}, Description: {db_record.description}"
        
        # If there's an uploaded file, extract its text content
        if db_record.file_url:
            filename = db_record.file_url.split('/')[-1]
            file_path = os.path.join(UPLOAD_DIR, filename)
            
            if os.path.exists(file_path):
                extracted_text = extract_text_from_file(file_path)
                if extracted_text:
                    # Append extracted file content to the record
                    content += f"\n\nExtracted File Content:\n{extracted_text}"
                    logger.info(f"Extracted {len(extracted_text)} characters from {filename}")
        
        # Upsert to RAG with complete content
        rag_service.upsert_data(
            user_id=current_user.id,
            data_type="health_record",
            content=content,
            metadata={"record_id": db_record.id}
        )
        logger.info(f"Successfully indexed health record {db_record.id} to RAG")
    except Exception as e:
        logger.error(f"Error triggering RAG ingestion: {e}")

    return db_record

@router.get("/health-records", response_model=List[HealthRecordResponse])
async def get_user_health_records(
    record_type: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all health records for current user
    """
    query = db.query(HealthRecord).filter(HealthRecord.user_id == current_user.id)
    if record_type:
        query = query.filter(HealthRecord.record_type == record_type)
    records = query.order_by(HealthRecord.record_date.desc()).all()
    return records

@router.get("/health-records/detail/{record_id}", response_model=HealthRecordResponse)
async def get_health_record(
    record_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific health record
    """
    record = db.query(HealthRecord).filter(
        HealthRecord.id == record_id,
        HealthRecord.user_id == current_user.id
    ).first()
    
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
    record = db.query(HealthRecord).filter(
        HealthRecord.id == record_id,
        HealthRecord.user_id == current_user.id
    ).first()
    
    if not record:
        raise HTTPException(status_code=404, detail="Health record not found")
    
    # Delete associated file if exists
    if record.file_url:
        filename = record.file_url.split('/')[-1]
        file_path = os.path.join(UPLOAD_DIR, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
    
    db.delete(record)
    db.commit()
    return {"message": "Health record deleted successfully"}
