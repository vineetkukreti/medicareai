from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta
from app.core.database import get_db
from app.core.security import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app import models, schemas
from app.services.email_service import send_email

router = APIRouter()

# Hardcoded admin credentials
ADMIN_EMAIL = "admin@gmail.com"
ADMIN_PASSWORD = "admin"

@router.post("/login", response_model=schemas.Token)
def admin_login(credentials: schemas.AdminLoginRequest):
    """Admin login endpoint with hardcoded credentials"""
    if credentials.email != ADMIN_EMAIL or credentials.password != ADMIN_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin credentials",
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": credentials.email, "role": "admin"}, 
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users", response_model=List[schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    """Get all registered users - Admin only"""
    users = db.query(models.User).order_by(models.User.created_at.desc()).all()
    return users

@router.get("/contacts", response_model=List[schemas.ContactResponse])
def get_all_contacts(db: Session = Depends(get_db)):
    """Get all contact form submissions - Admin only"""
    contacts = db.query(models.ContactMessage).order_by(models.ContactMessage.created_at.desc()).all()
    return contacts

@router.post("/reply-contact/{contact_id}")
async def reply_to_contact(contact_id: int, reply_data: schemas.AdminReplyRequest, db: Session = Depends(get_db)):
    """Send email reply to a contact inquiry and mark as resolved"""
    # Get the contact message
    contact = db.query(models.ContactMessage).filter(models.ContactMessage.id == contact_id).first()
    
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact message not found"
        )
    
    # Send email reply
    try:
        subject = f"Re: Your inquiry to MediCareAI"
        body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <div style="background: linear-gradient(135deg, #0066CC 0%, #06B6D4 100%); padding: 30px; border-radius: 10px 10px 0 0;">
                        <h1 style="color: white; margin: 0; font-size: 24px;">MediCareAI</h1>
                        <p style="color: #E0F2FE; margin: 5px 0 0 0;">Your AI-Powered Health Companion</p>
                    </div>
                    
                    <div style="background: #f9fafb; padding: 30px; border-radius: 0 0 10px 10px;">
                        <p style="margin-top: 0;">Dear {contact.name},</p>
                        
                        <p>Thank you for reaching out to MediCareAI. Here's our response to your inquiry:</p>
                        
                        <div style="background: white; padding: 20px; border-left: 4px solid #0066CC; margin: 20px 0; border-radius: 5px;">
                            <p style="margin: 0; white-space: pre-wrap;">{reply_data.message}</p>
                        </div>
                        
                        <p style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #e5e7eb;">
                            <strong>Your Original Message:</strong><br>
                            <em style="color: #6b7280;">{contact.message}</em>
                        </p>
                        
                        <p style="margin-top: 30px;">
                            If you have any further questions, please don't hesitate to contact us.
                        </p>
                        
                        <p style="margin-bottom: 0;">
                            Best regards,<br>
                            <strong>MediCareAI Support Team</strong>
                        </p>
                    </div>
                    
                    <div style="text-align: center; margin-top: 20px; color: #6b7280; font-size: 12px;">
                        <p>This email was sent by MediCareAI - Your AI-Powered Health Companion</p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        send_email(contact.email, subject, body)
        
        # Delete the contact after successful reply (mark as resolved)
        db.delete(contact)
        db.commit()
        
        return {
            "success": True,
            "message": f"Reply sent successfully to {contact.email} and inquiry marked as resolved"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send email: {str(e)}"
        )

@router.delete("/contact/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    """Delete a contact inquiry - Admin only"""
    contact = db.query(models.ContactMessage).filter(models.ContactMessage.id == contact_id).first()
    
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact message not found"
        )
    
    db.delete(contact)
    db.commit()
    
    return {
        "success": True,
        "message": "Contact inquiry deleted successfully"
    }
