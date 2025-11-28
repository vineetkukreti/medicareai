#!/usr/bin/env python3
"""
Update .env file with email credentials
"""
import os
from pathlib import Path

def update_env_with_email():
    """Interactive script to update .env with email credentials."""
    
    print("\n" + "="*70)
    print("📧 KisanAI Email Configuration Setup")
    print("="*70 + "\n")
    
    print("This script will help you configure Gmail SMTP for email notifications.\n")
    
    # Get credentials from user
    print("📝 Enter your Gmail credentials:")
    print("   (Get App Password from: https://myaccount.google.com/apppasswords)\n")
    
    smtp_user = input("Gmail address: ").strip()
    if not smtp_user:
        print("❌ Gmail address is required!")
        return
    
    smtp_password = input("Gmail App Password (16 characters): ").strip()
    if not smtp_password:
        print("❌ App Password is required!")
        return
    
    from_name = input("From Name [KisanAI]: ").strip()
    if not from_name:
        from_name = "KisanAI"
    
    # Read current .env file
    env_path = Path(__file__).parent / ".env"
    
    try:
        with open(env_path, "r") as f:
            env_content = f.read()
    except FileNotFoundError:
        print("❌ .env file not found!")
        return
    
    # Update email configuration
    lines = env_content.split('\n')
    updated_lines = []
    email_section_found = False
    
    for line in lines:
        if line.startswith("SMTP_USER="):
            updated_lines.append(f"SMTP_USER={smtp_user}")
            email_section_found = True
        elif line.startswith("SMTP_PASSWORD="):
            updated_lines.append(f"SMTP_PASSWORD={smtp_password}")
        elif line.startswith("FROM_EMAIL="):
            updated_lines.append(f"FROM_EMAIL={smtp_user}")
        elif line.startswith("FROM_NAME="):
            updated_lines.append(f"FROM_NAME={from_name}")
        else:
            updated_lines.append(line)
    
    # If email section not found, add it
    if not email_section_found:
        email_config = f"""
# Email Configuration (Gmail SMTP)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER={smtp_user}
SMTP_PASSWORD={smtp_password}
FROM_EMAIL={smtp_user}
FROM_NAME={from_name}
"""
        updated_lines.append(email_config)
    
    # Write updated content
    with open(env_path, "w") as f:
        f.write('\n'.join(updated_lines))
    
    print("\n✅ .env file updated successfully!")
    print("\n📋 Email Configuration:")
    print(f"   SMTP User: {smtp_user}")
    print(f"   SMTP Password: {smtp_password[:4]}...{smtp_password[-4:]}")
    print(f"   From Name: {from_name}")
    
    print("\n🔄 Next steps:")
    print("   1. Restart your backend server")
    print("   2. Run: python test_email.py")
    print("   3. Test signup and login to verify emails are sent")
    print("\nSee EMAIL_SETUP.md for detailed instructions.")

if __name__ == "__main__":
    update_env_with_email()
