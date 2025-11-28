"""
SMS Notification Service using Twilio
Sends SMS notifications for contact form submissions.
"""
from typing import Optional
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from app.core.config import settings
import logging

# Set up logging
logger = logging.getLogger(__name__)


class SMSService:
    """Service for sending SMS notifications via Twilio."""
    
    def __init__(self):
        """Initialize Twilio client if credentials are configured."""
        self.client: Optional[Client] = None
        self.is_enabled = settings.is_twilio_configured
        
        if self.is_enabled:
            try:
                self.client = Client(
                    settings.TWILIO_ACCOUNT_SID,
                    settings.TWILIO_AUTH_TOKEN
                )
                logger.info("✅ Twilio SMS service initialized successfully")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Twilio client: {e}")
                self.is_enabled = False
        else:
            logger.warning("⚠️  SMS notifications disabled - Twilio not configured")
    
    def send_contact_notification(
        self,
        contact_name: str,
        contact_email: str,
        contact_message: str
    ) -> bool:
        """
        Send SMS notification about new contact form submission.
        
        Args:
            contact_name: Name of the person who submitted the form
            contact_email: Email of the person who submitted the form
            contact_message: Message content from the form
            
        Returns:
            bool: True if SMS was sent successfully, False otherwise
        """
        if not self.is_enabled or not self.client:
            logger.warning("SMS notification skipped - service not enabled")
            return False
        
        try:
            # Format the SMS message
            message_preview = contact_message[:100] + "..." if len(contact_message) > 100 else contact_message
            
            sms_body = f"""❤️ MediCareAI - New Contact Form Submission

Name: {contact_name}
Email: {contact_email}

Message:
{message_preview}

---
Reply to contact them directly."""
            
            # Send SMS via Twilio
            message = self.client.messages.create(
                body=sms_body,
                from_=settings.TWILIO_PHONE_NUMBER,
                to=settings.ADMIN_PHONE_NUMBER
            )
            
            logger.info(f"✅ SMS sent successfully! SID: {message.sid}")
            logger.info(f"   To: {settings.ADMIN_PHONE_NUMBER}")
            logger.info(f"   From: {contact_name} ({contact_email})")
            
            return True
            
        except TwilioRestException as e:
            logger.error(f"❌ Twilio API error: {e.msg}")
            logger.error(f"   Error code: {e.code}")
            return False
            
        except Exception as e:
            logger.error(f"❌ Unexpected error sending SMS: {e}")
            return False
    
    def send_test_sms(self) -> bool:
        """
        Send a test SMS to verify configuration.
        
        Returns:
            bool: True if test SMS was sent successfully
        """
        if not self.is_enabled or not self.client:
            logger.error("Cannot send test SMS - service not enabled")
            return False
        
        try:
            message = self.client.messages.create(
                body="❤️ MediCareAI SMS Test - Your SMS notifications are working perfectly! ✅",
                from_=settings.TWILIO_PHONE_NUMBER,
                to=settings.ADMIN_PHONE_NUMBER
            )
            
            logger.info(f"✅ Test SMS sent! SID: {message.sid}")
            return True
            
        except TwilioRestException as e:
            logger.error(f"❌ Test SMS failed: {e.msg}")
            return False


# Create global SMS service instance
sms_service = SMSService()
