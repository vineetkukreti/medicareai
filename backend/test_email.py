#!/usr/bin/env python3
"""
Email Service Test Script
Tests the email configuration and sends a test email.
"""
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.config import settings
from app.services.email_service import email_service


def test_email_configuration():
    """Test email service configuration and send test email."""
    
    print("\n" + "="*60)
    print("📧 MediCareAI Email Service Test")
    print("="*60 + "\n")
    
    # Check configuration
    print("📋 Configuration Check:")
    print(f"   SMTP Host: {settings.SMTP_HOST}")
    print(f"   SMTP Port: {settings.SMTP_PORT}")
    print(f"   SMTP User: {settings.SMTP_USER}")
    print(f"   From Email: {settings.FROM_EMAIL}")
    print(f"   From Name: {settings.FROM_NAME}")
    print(f"   Password Set: {'✅ Yes' if settings.SMTP_PASSWORD else '❌ No'}")
    print(f"   Service Enabled: {'✅ Yes' if settings.is_email_configured else '❌ No'}\n")
    
    if not settings.is_email_configured:
        print("❌ Email service is NOT configured!")
        print("\n📝 To configure email service:")
        print("   1. Get Gmail App Password: https://myaccount.google.com/apppasswords")
        print("   2. Update .env file with:")
        print("      SMTP_USER=your-email@gmail.com")
        print("      SMTP_PASSWORD=your-16-char-app-password")
        print("      FROM_EMAIL=your-email@gmail.com")
        print("\n   See SETUP_SERVICES.md for detailed instructions.")
        return False
    
    # Get test email address
    print("="*60)
    test_email = input("📬 Enter email address to send test to (or press Enter to use SMTP_USER): ").strip()
    
    if not test_email:
        test_email = settings.SMTP_USER
    
    print(f"\n📤 Sending test email to: {test_email}")
    print("⏳ Please wait...\n")
    
    # Send test email
    success = email_service.send_test_email(test_email)
    
    print("\n" + "="*60)
    if success:
        print("✅ SUCCESS! Test email sent successfully!")
        print(f"📬 Check your inbox at: {test_email}")
        print("\n💡 Email service is working correctly!")
    else:
        print("❌ FAILED! Could not send test email.")
        print("\n🔍 Common issues:")
        print("   • Using regular Gmail password instead of App Password")
        print("   • 2-Factor Authentication not enabled on Gmail")
        print("   • Incorrect SMTP credentials in .env file")
        print("   • Network/firewall blocking SMTP connection")
        print("\n📖 See SETUP_SERVICES.md for troubleshooting.")
    print("="*60 + "\n")
    
    return success


if __name__ == "__main__":
    try:
        test_email_configuration()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
