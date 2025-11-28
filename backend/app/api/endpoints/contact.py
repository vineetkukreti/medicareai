from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app import models, schemas
from app.services.sms_service import sms_service
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/contact", response_model=schemas.Contact)
def submit_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    """
    Submit a contact form message.
    Saves to database and sends SMS notification to admin.
    """
    # Save to database
    db_contact = models.ContactMessage(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    
    logger.info(f"📝 New contact form submission from {contact.email}")
    
    # Send SMS notification to admin
    try:
        sms_sent = sms_service.send_contact_notification(
            contact_name=contact.name,
            contact_email=contact.email,
            contact_message=contact.message
        )
        
        if sms_sent:
            logger.info("📱 SMS notification sent to admin successfully")
        else:
            logger.warning("⚠️  SMS notification failed, but contact saved to database")
            
    except Exception as e:
        # Don't fail the contact submission if SMS fails
        logger.error(f"❌ Error sending SMS notification: {e}")
        logger.info("✅ Contact form submission saved despite SMS error")
    
    return db_contact

    
    return db_contact
