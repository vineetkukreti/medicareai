"""
Configuration management for MediCareAI application.
Loads and validates environment variables.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Application settings loaded from environment variables."""
    
    PROJECT_NAME: str = "MediCareAI"
    API_V1_STR: str = "/api/v1"
    
    # Twilio Configuration
    TWILIO_ACCOUNT_SID: str = os.getenv("TWILIO_ACCOUNT_SID", "")
    TWILIO_AUTH_TOKEN: str = os.getenv("TWILIO_AUTH_TOKEN", "")
    TWILIO_PHONE_NUMBER: str = os.getenv("TWILIO_PHONE_NUMBER", "")
    
    # Admin Configuration
    ADMIN_PHONE_NUMBER: str = os.getenv("ADMIN_PHONE_NUMBER", "+917983207219")
    
    # Database Configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./kisanai.db")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "default-secret-key-change-in-production")
    
    # Application Settings
    APP_NAME: str = os.getenv("APP_NAME", "MediCareAI")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # Email Configuration (Gmail SMTP)
    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    FROM_EMAIL: str = os.getenv("FROM_EMAIL", "")
    FROM_NAME: str = os.getenv("FROM_NAME", "MediCareAI")
    
    @property
    def is_twilio_configured(self) -> bool:
        """Check if Twilio credentials are properly configured."""
        return bool(
            self.TWILIO_ACCOUNT_SID and 
            self.TWILIO_ACCOUNT_SID != "your_twilio_account_sid_here" and
            self.TWILIO_AUTH_TOKEN and 
            self.TWILIO_AUTH_TOKEN != "your_twilio_auth_token_here" and
            self.TWILIO_PHONE_NUMBER and
            self.TWILIO_PHONE_NUMBER != "+1234567890"
        )
    
    @property
    def is_email_configured(self) -> bool:
        """Check if email SMTP credentials are properly configured."""
        return bool(
            self.SMTP_USER and
            self.SMTP_USER != "your-email@gmail.com" and
            self.SMTP_PASSWORD and
            self.SMTP_PASSWORD != "your-app-password-here" and
            self.FROM_EMAIL and
            self.FROM_EMAIL != "your-email@gmail.com"
        )
    
    def validate(self) -> None:
        """Validate critical configuration settings."""
        if not self.SECRET_KEY or self.SECRET_KEY == "default-secret-key-change-in-production":
            print("⚠️  WARNING: Using default SECRET_KEY. Change this in production!")
        
        if not self.is_twilio_configured:
            print("⚠️  WARNING: Twilio is not configured. SMS notifications will be disabled.")
            print("   To enable SMS notifications:")
            print("   1. Sign up at https://www.twilio.com/try-twilio")
            print("   2. Update .env file with your Twilio credentials")
        
        if not self.is_email_configured:
            print("⚠️  WARNING: Email is not configured. Email notifications will be disabled.")
            print("   To enable email notifications:")
            print("   1. Get Gmail App Password: https://myaccount.google.com/apppasswords")
            print("   2. Update .env file with your email credentials")

settings = Settings()

# Validate settings on import
settings.validate()
