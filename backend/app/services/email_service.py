"""
Email Service for MediCareAI
Sends transactional emails using Gmail SMTP
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from datetime import datetime
import logging

from app.core.config import settings
from app.services.email_templates import (
    get_welcome_email_html,
    get_welcome_email_subject,
    get_login_alert_email_html,
    get_login_alert_subject
)

# Set up logging
logger = logging.getLogger(__name__)


class EmailService:
    """Service for sending emails via SMTP."""
    
    def __init__(self):
        """Initialize email service with SMTP configuration."""
        self.is_enabled = settings.is_email_configured
        
        if self.is_enabled:
            logger.info("✅ Email service initialized successfully")
        else:
            logger.warning("⚠️  Email notifications disabled - SMTP not configured")
    
    def _send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str
    ) -> bool:
        """
        Send an email via SMTP.
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            html_content: HTML email content
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        if not self.is_enabled:
            logger.warning("Email service not enabled, skipping email send")
            return False
        
        try:
            # Create message
            message = MIMEMultipart('alternative')
            message['Subject'] = subject
            message['From'] = f"{settings.FROM_NAME} <{settings.FROM_EMAIL}>"
            message['To'] = to_email
            
            # Attach HTML content
            html_part = MIMEText(html_content, 'html')
            message.attach(html_part)
            
            # Connect to SMTP server and send
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.starttls()  # Secure the connection
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(message)
            
            logger.info(f"✅ Email sent successfully to {to_email}")
            logger.info(f"   Subject: {subject}")
            return True
            
        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"❌ SMTP Authentication failed: {e}")
            logger.error("   Check your SMTP_USER and SMTP_PASSWORD in .env file")
            return False
            
        except smtplib.SMTPException as e:
            logger.error(f"❌ SMTP error: {e}")
            return False
            
        except Exception as e:
            logger.error(f"❌ Unexpected error sending email: {e}")
            return False
    
    def send_welcome_email(self, user_name: str, user_email: str) -> bool:
        """
        Send welcome email to new user.
        
        Args:
            user_name: Name of the new user
            user_email: Email of the new user
            
        Returns:
            bool: True if email sent successfully
        """
        logger.info(f"📧 Sending welcome email to {user_email}")
        
        subject = get_welcome_email_subject()
        html_content = get_welcome_email_html(user_name, user_email)
        
        return self._send_email(user_email, subject, html_content)
    
    def send_login_alert_email(self, user_name: str, user_email: str) -> bool:
        """
        Send login alert email for security notification.
        
        Args:
            user_name: Name of the user
            user_email: Email of the user
            
        Returns:
            bool: True if email sent successfully
        """
        logger.info(f"🔐 Sending login alert email to {user_email}")
        
        # Get current timestamp
        login_time = datetime.now().strftime("%B %d, %Y at %I:%M %p IST")
        
        subject = get_login_alert_subject()
        html_content = get_login_alert_email_html(user_name, user_email, login_time)
        
        return self._send_email(user_email, subject, html_content)
    
    def send_test_email(self, to_email: str) -> bool:
        """
        Send a test email to verify configuration.
        
        Args:
            to_email: Email address to send test to
            
        Returns:
            bool: True if test email sent successfully
        """
        if not self.is_enabled:
            logger.error("Cannot send test email - service not enabled")
            return False
        
        subject = "❤️ MediCareAI Email Test"
        html_content = """
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h2>✅ Email Service is Working!</h2>
            <p>This is a test email from your MediCareAI application.</p>
            <p>If you received this, your email configuration is correct!</p>
            <br>
            <p>Best regards,<br><strong>MediCareAI Team</strong></p>
        </body>
        </html>
        """
        
        return self._send_email(to_email, subject, html_content)


email_service = EmailService()

def send_email(to_email: str, subject: str, html_content: str) -> bool:
    """Compatibility wrapper to send email using the global EmailService instance.
    This mirrors the previous API that admin endpoint expects.
    """
    return email_service._send_email(to_email, subject, html_content)
