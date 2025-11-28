from sqlalchemy.orm import Session
from app.modules.contact import models, schemas
from app.services.sms_service import sms_service
from app.services.email_service import send_email

class ContactService:
    def create_contact(self, db: Session, contact: schemas.ContactCreate):
        db_contact = models.ContactMessage(**contact.dict())
        db.add(db_contact)
        db.commit()
        db.refresh(db_contact)
        return db_contact

    def send_admin_notification(self, contact: schemas.ContactCreate):
        return sms_service.send_contact_notification(
            contact_name=contact.name,
            contact_email=contact.email,
            contact_message=contact.message
        )

    def get_all_contacts(self, db: Session):
        return db.query(models.ContactMessage).order_by(models.ContactMessage.created_at.desc()).all()

    def get_contact_by_id(self, db: Session, contact_id: int):
        return db.query(models.ContactMessage).filter(models.ContactMessage.id == contact_id).first()

    def delete_contact(self, db: Session, contact: models.ContactMessage):
        db.delete(contact)
        db.commit()

    def reply_to_contact(self, db: Session, contact: models.ContactMessage, message: str):
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
                            <p style="margin: 0; white-space: pre-wrap;">{message}</p>
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
        self.delete_contact(db, contact)

contact_service = ContactService()
