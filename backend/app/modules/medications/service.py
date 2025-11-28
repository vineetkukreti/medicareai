from sqlalchemy.orm import Session
from app.modules.medications import models, schemas
from app.services.rag_service import rag_service
from typing import List

class MedicationService:
    def create_medication(self, db: Session, medication: schemas.MedicationCreate, user_id: int, background_tasks=None):
        db_medication = models.Medication(**medication.dict(), user_id=user_id)
        db.add(db_medication)
        db.commit()
        db.refresh(db_medication)
        
        # Trigger RAG ingestion in background
        if background_tasks:
            background_tasks.add_task(
                self._index_medication_to_rag,
                user_id=user_id,
                medication_id=db_medication.id,
                medication_name=db_medication.medication_name,
                dosage=db_medication.dosage,
                frequency=db_medication.frequency,
                start_date=str(db_medication.start_date),
                notes=db_medication.notes
            )
            
        return db_medication
    
    def _index_medication_to_rag(self, user_id, medication_id, medication_name, dosage, frequency, start_date, notes):
        """Background task to index medication to RAG"""
        try:
            content = f"Medication: {medication_name}, Dosage: {dosage}, Frequency: {frequency}, Start Date: {start_date}, Notes: {notes}"
            rag_service.upsert_data(
                user_id=user_id,
                data_type="medication",
                content=content,
                metadata={"medication_id": medication_id}
            )
        except Exception as e:
            print(f"Error triggering RAG ingestion: {e}")

    def get_user_medications(self, db: Session, user_id: int, active_only: bool = True):
        query = db.query(models.Medication).filter(models.Medication.user_id == user_id)
        if active_only:
            query = query.filter(models.Medication.is_active == True)
        return query.all()

    def get_medication_by_id(self, db: Session, medication_id: int):
        return db.query(models.Medication).filter(models.Medication.id == medication_id).first()

    def update_medication(self, db: Session, medication_id: int, medication_data: schemas.MedicationCreate):
        db_medication = self.get_medication_by_id(db, medication_id)
        if not db_medication:
            return None
        
        for key, value in medication_data.dict().items():
            setattr(db_medication, key, value)
        
        db.commit()
        db.refresh(db_medication)
        return db_medication

    def delete_medication(self, db: Session, medication_id: int, user_id: int):
        db_medication = self.get_medication_by_id(db, medication_id)
        if not db_medication:
            return False
        
        # Delete from RAG when deactivating
        try:
            rag_service.delete_by_metadata(
                user_id=user_id,
                data_type="medication",
                metadata_key="medication_id",
                metadata_value=medication_id
            )
        except Exception as e:
            print(f"Error deleting from RAG: {e}")
        
        db_medication.is_active = False
        db.commit()
        return True

medication_service = MedicationService()
