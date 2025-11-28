#!/usr/bin/env python3
"""
SMS Service Test Script
Tests the Twilio SMS configuration and sends a test SMS.
"""
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.config import settings
from app.services.sms_service import sms_service


def test_sms_configuration():
    """Test SMS service configuration and send test SMS."""
    
    print("\n" + "="*60)
    print("📱 MediCareAI SMS Service Test")
    print("="*60 + "\n")
    
    # Check configuration
    print("📋 Configuration Check:")
    print(f"   Twilio Account SID: {settings.TWILIO_ACCOUNT_SID[:10]}..." if settings.TWILIO_ACCOUNT_SID else "   Twilio Account SID: Not set")
    print(f"   Auth Token Set: {'✅ Yes' if settings.TWILIO_AUTH_TOKEN else '❌ No'}")
    print(f"   Twilio Phone: {settings.TWILIO_PHONE_NUMBER}")
    print(f"   Admin Phone: {settings.ADMIN_PHONE_NUMBER}")
    print(f"   Service Enabled: {'✅ Yes' if settings.is_twilio_configured else '❌ No'}\n")
    
    if not settings.is_twilio_configured:
        print("❌ SMS service is NOT configured!")
        print("\n📝 To configure SMS service:")
        print("   1. Sign up at: https://www.twilio.com/try-twilio")
        print("   2. Get your credentials from: https://console.twilio.com/")
        print("   3. Update .env file with:")
        print("      TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        print("      TWILIO_AUTH_TOKEN=your_auth_token")
        print("      TWILIO_PHONE_NUMBER=+1234567890")
        print("\n   4. For trial accounts, verify your phone number at:")
        print("      https://console.twilio.com/us1/develop/phone-numbers/manage/verified")
        print("\n   See SETUP_SERVICES.md for detailed instructions.")
        return False
    
    print("="*60)
    print(f"📤 Sending test SMS to: {settings.ADMIN_PHONE_NUMBER}")
    print("⏳ Please wait...\n")
    
    # Send test SMS
    success = sms_service.send_test_sms()
    
    print("\n" + "="*60)
    if success:
        print("✅ SUCCESS! Test SMS sent successfully!")
        print(f"📱 Check your phone: {settings.ADMIN_PHONE_NUMBER}")
        print("\n💡 SMS service is working correctly!")
        print("\n⚠️  Note: Trial accounts show 'Sent from Twilio trial account' prefix")
    else:
        print("❌ FAILED! Could not send test SMS.")
        print("\n🔍 Common issues:")
        print("   • Phone number not verified (required for trial accounts)")
        print("   • Incorrect Twilio credentials in .env file")
        print("   • Invalid phone number format (must include country code)")
        print("   • Insufficient Twilio credit")
        print("\n📖 See SETUP_SERVICES.md for troubleshooting.")
        print("\n🔗 Check Twilio console for detailed error:")
        print("   https://console.twilio.com/us1/monitor/logs/sms")
    print("="*60 + "\n")
    
    return success


if __name__ == "__main__":
    try:
        test_sms_configuration()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
