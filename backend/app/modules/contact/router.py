from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.modules.contact import schemas
from app.modules.contact.service import contact_service
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
    db_contact = contact_service.create_contact(db, contact)
    
    logger.info(f"📝 New contact form submission from {contact.email}")
    
    # Send SMS notification to admin
    try:
        sms_sent = contact_service.send_admin_notification(contact)
        
        if sms_sent:
            logger.info("📱 SMS notification sent to admin successfully")
        else:
            logger.warning("⚠️  SMS notification failed, but contact saved to database")
            
    except Exception as e:
        # Don't fail the contact submission if SMS fails
        logger.error(f"❌ Error sending SMS notification: {e}")
        logger.info("✅ Contact form submission saved despite SMS error")
    
    return db_contact

# Admin endpoints for contact
@router.get("/admin/contacts", response_model=List[schemas.ContactResponse])
def get_all_contacts(db: Session = Depends(get_db)):
    """Get all contact form submissions - Admin only"""
    return contact_service.get_all_contacts(db)

@router.post("/admin/reply-contact/{contact_id}")
async def reply_to_contact(contact_id: int, reply_data: schemas.AdminReplyRequest, db: Session = Depends(get_db)):
    """Send email reply to a contact inquiry and mark as resolved"""
    contact = contact_service.get_contact_by_id(db, contact_id)
    
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact message not found"
        )
    
    try:
        contact_service.reply_to_contact(db, contact, reply_data.message)
        return {
            "success": True,
            "message": f"Reply sent successfully to {contact.email} and inquiry marked as resolved"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send email: {str(e)}"
        )

@router.delete("/admin/contact/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    """Delete a contact inquiry - Admin only"""
    contact = contact_service.get_contact_by_id(db, contact_id)
    
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact message not found"
        )
    
    contact_service.delete_contact(db, contact)
    
    return {
        "success": True,
        "message": "Contact inquiry deleted successfully"
    }
