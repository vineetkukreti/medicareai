from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException
from app.modules.health_records import models, schemas
from app.services.rag_service import rag_service
import os
import shutil
from datetime import datetime
import PyPDF2
import logging
from typing import Optional

logger = logging.getLogger(__name__)

UPLOAD_DIR = "uploads/health_records"
ALLOWED_EXTENSIONS = {'.pdf', '.jpg', '.jpeg', '.png', '.docx', '.doc'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

class HealthRecordService:
    def __init__(self):
        os.makedirs(UPLOAD_DIR, exist_ok=True)

    def extract_text_from_file(self, file_path: str) -> Optional[str]:
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
            
            return None
        except Exception as e:
            logger.error(f"Error extracting text from {file_path}: {e}")
            return None

    async def upload_file(self, file: UploadFile, user_id: int):
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
        safe_filename = f"{user_id}_{timestamp}_{file.filename}"
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

    def create_health_record(self, db: Session, record: schemas.HealthRecordCreate, user_id: int):
        db_record = models.HealthRecord(**record.dict(), user_id=user_id)
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
                    extracted_text = self.extract_text_from_file(file_path)
                    if extracted_text:
                        # Append extracted file content to the record
                        content += f"\n\nExtracted File Content:\n{extracted_text}"
                        logger.info(f"Extracted {len(extracted_text)} characters from {filename}")
            
            # Upsert to RAG with complete content
            rag_service.upsert_data(
                user_id=user_id,
                data_type="health_record",
                content=content,
                metadata={"record_id": db_record.id}
            )
            logger.info(f"Successfully indexed health record {db_record.id} to RAG")
        except Exception as e:
            logger.error(f"Error triggering RAG ingestion: {e}")

        return db_record

    def get_user_health_records(self, db: Session, user_id: int, record_type: str = None):
        query = db.query(models.HealthRecord).filter(models.HealthRecord.user_id == user_id)
        if record_type:
            query = query.filter(models.HealthRecord.record_type == record_type)
        return query.order_by(models.HealthRecord.record_date.desc()).all()

    def get_health_record_by_id(self, db: Session, record_id: int, user_id: int):
        return db.query(models.HealthRecord).filter(
            models.HealthRecord.id == record_id,
            models.HealthRecord.user_id == user_id
        ).first()

    def delete_health_record(self, db: Session, record_id: int, user_id: int):
        record = self.get_health_record_by_id(db, record_id, user_id)
        if not record:
            return False
        
        # Delete from RAG first
        try:
            rag_service.delete_by_metadata(
                user_id=user_id,
                data_type="health_record",
                metadata_key="record_id",
                metadata_value=record_id
            )
            logger.info(f"Deleted health record {record_id} from RAG")
        except Exception as e:
            logger.error(f"Error deleting from RAG: {e}")
        
        # Delete associated file if exists
        if record.file_url:
            filename = record.file_url.split('/')[-1]
            file_path = os.path.join(UPLOAD_DIR, filename)
            if os.path.exists(file_path):
                os.remove(file_path)
        
        db.delete(record)
        db.commit()
        return True

health_record_service = HealthRecordService()
