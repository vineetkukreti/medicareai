#!/usr/bin/env python3
"""
Update .env file with Twilio credentials
"""
import os
from pathlib import Path

# Twilio credentials
ACCOUNT_SID = "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
AUTH_TOKEN = "your_auth_token_here"
ADMIN_PHONE = "+91xxxxxxxxxx"

# Note: User needs to get a phone number from Twilio first
TWILIO_PHONE = "+1234567890"  # Placeholder - needs to be updated

env_content = f"""# Environment Configuration
# Updated with Twilio credentials

# Twilio SMS Configuration
TWILIO_ACCOUNT_SID={ACCOUNT_SID}
TWILIO_AUTH_TOKEN={AUTH_TOKEN}
TWILIO_PHONE_NUMBER={TWILIO_PHONE}

# Admin Contact Information
ADMIN_PHONE_NUMBER={ADMIN_PHONE}

# Database Configuration
DATABASE_URL=sqlite:///./kisanai.db

# Security
SECRET_KEY=kisanai-secret-key-change-in-production-2024

# Application Settings
APP_NAME=KisanAI
DEBUG=True
"""

# Write to .env file
env_path = Path(__file__).parent / ".env"
with open(env_path, "w") as f:
    f.write(env_content)

print("✅ .env file updated with your credentials!")
print("\n⚠️  IMPORTANT: You still need to get a Twilio phone number!")
print("\nFollow these steps:")
print("1. Go to: https://console.twilio.com/us1/develop/phone-numbers/manage/search")
print("2. Select country: United States (or India if available)")
print("3. Click 'Search' to find available numbers")
print("4. Click 'Buy' on any number (it's FREE with trial)")
print("5. Copy the phone number (format: +1234567890)")
print("6. Update TWILIO_PHONE_NUMBER in .env file")
print("\nAfter getting the number, restart your backend and run: python test_sms.py")
