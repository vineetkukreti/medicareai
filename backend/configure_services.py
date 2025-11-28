#!/usr/bin/env python3
"""
Interactive Service Configuration Script
Helps configure Email and SMS services for MediCareAI
"""
import os
import re
from pathlib import Path


def get_env_path():
    """Get the path to the .env file."""
    backend_dir = Path(__file__).parent
    return backend_dir / ".env"


def read_env_file():
    """Read current .env file contents."""
    env_path = get_env_path()
    if env_path.exists():
        with open(env_path, 'r') as f:
            return f.read()
    return ""


def update_env_variable(env_content, key, value):
    """Update or add an environment variable."""
    pattern = f"^{key}=.*$"
    replacement = f"{key}={value}"
    
    if re.search(pattern, env_content, re.MULTILINE):
        # Update existing
        return re.sub(pattern, replacement, env_content, flags=re.MULTILINE)
    else:
        # Add new
        return env_content + f"\n{replacement}"


def write_env_file(content):
    """Write updated content to .env file."""
    env_path = get_env_path()
    with open(env_path, 'w') as f:
        f.write(content)


def validate_email(email):
    """Basic email validation."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone):
    """Basic phone number validation."""
    # Should start with + and contain only digits
    pattern = r'^\+[1-9]\d{1,14}$'
    return re.match(pattern, phone) is not None


def configure_email():
    """Interactive email configuration."""
    print("\n" + "="*60)
    print("📧 Email Service Configuration (Gmail)")
    print("="*60)
    
    print("\n📝 You'll need:")
    print("   • A Gmail account")
    print("   • Gmail App Password (NOT your regular password)")
    print("\n🔗 Get App Password: https://myaccount.google.com/apppasswords")
    print("   (Requires 2-Factor Authentication enabled)")
    
    input("\nPress Enter when ready to continue...")
    
    # Get email
    while True:
        email = input("\n📧 Enter your Gmail address: ").strip()
        if validate_email(email):
            break
        print("❌ Invalid email format. Please try again.")
    
    # Get app password
    while True:
        app_password = input("🔑 Enter your Gmail App Password (16 characters): ").strip()
        # Remove spaces if user copied with spaces
        app_password = app_password.replace(" ", "")
        if len(app_password) == 16:
            break
        print("❌ App Password should be 16 characters. Please try again.")
    
    # Get from name
    from_name = input("👤 Enter sender name (default: MediCareAI): ").strip()
    if not from_name:
        from_name = "MediCareAI"
    
    return {
        'SMTP_USER': email,
        'SMTP_PASSWORD': app_password,
        'FROM_EMAIL': email,
        'FROM_NAME': from_name
    }


def configure_sms():
    """Interactive SMS configuration."""
    print("\n" + "="*60)
    print("📱 SMS Service Configuration (Twilio)")
    print("="*60)
    
    print("\n📝 You'll need:")
    print("   • Twilio account (free $15 credit)")
    print("   • Account SID")
    print("   • Auth Token")
    print("   • Twilio phone number")
    
    print("\n🔗 Sign up: https://www.twilio.com/try-twilio")
    print("🔗 Get credentials: https://console.twilio.com/")
    
    input("\nPress Enter when ready to continue...")
    
    # Get Account SID
    while True:
        account_sid = input("\n🔑 Enter Twilio Account SID (starts with AC): ").strip()
        if account_sid.startswith("AC") and len(account_sid) == 34:
            break
        print("❌ Invalid Account SID format. Should start with 'AC' and be 34 characters.")
    
    # Get Auth Token
    auth_token = input("🔑 Enter Twilio Auth Token (32 characters): ").strip()
    
    # Get Twilio phone number
    while True:
        twilio_phone = input("📞 Enter Twilio phone number (with country code, e.g., +12345678901): ").strip()
        if validate_phone(twilio_phone):
            break
        print("❌ Invalid phone format. Should start with + and country code.")
    
    # Get admin phone number
    print("\n📱 Admin phone number (where notifications will be sent)")
    while True:
        admin_phone = input("📞 Enter your phone number (with country code, e.g., +917983207219): ").strip()
        if validate_phone(admin_phone):
            break
        print("❌ Invalid phone format. Should start with + and country code.")
    
    print("\n⚠️  IMPORTANT for Trial Accounts:")
    print(f"   You must verify {admin_phone} in Twilio console:")
    print("   https://console.twilio.com/us1/develop/phone-numbers/manage/verified")
    
    return {
        'TWILIO_ACCOUNT_SID': account_sid,
        'TWILIO_AUTH_TOKEN': auth_token,
        'TWILIO_PHONE_NUMBER': twilio_phone,
        'ADMIN_PHONE_NUMBER': admin_phone
    }


def main():
    """Main configuration flow."""
    print("\n" + "="*60)
    print("🔧 MediCareAI Services Configuration")
    print("="*60)
    
    print("\nThis script will help you configure:")
    print("   1. 📧 Email Service (Gmail)")
    print("   2. 📱 SMS Service (Twilio)")
    
    print("\nYou can configure one or both services.")
    
    # Read current .env
    env_content = read_env_file()
    if not env_content:
        print("\n❌ Error: .env file not found!")
        return
    
    updates = {}
    
    # Configure Email
    print("\n" + "-"*60)
    choice = input("\n📧 Configure Email Service? (y/n): ").strip().lower()
    if choice == 'y':
        email_config = configure_email()
        updates.update(email_config)
        print("\n✅ Email configuration captured!")
    
    # Configure SMS
    print("\n" + "-"*60)
    choice = input("\n📱 Configure SMS Service? (y/n): ").strip().lower()
    if choice == 'y':
        sms_config = configure_sms()
        updates.update(sms_config)
        print("\n✅ SMS configuration captured!")
    
    if not updates:
        print("\n⚠️  No changes made.")
        return
    
    # Apply updates
    print("\n" + "="*60)
    print("💾 Updating .env file...")
    
    for key, value in updates.items():
        env_content = update_env_variable(env_content, key, value)
        print(f"   ✓ {key}")
    
    write_env_file(env_content)
    
    print("\n✅ Configuration saved successfully!")
    print("\n📋 Next steps:")
    print("   1. Restart your backend server")
    print("   2. Test your configuration:")
    
    if any(k.startswith('SMTP') for k in updates.keys()):
        print("      python backend/test_email.py")
    
    if any(k.startswith('TWILIO') for k in updates.keys()):
        print("      python backend/test_sms.py")
    
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Configuration cancelled by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
