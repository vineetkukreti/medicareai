#!/usr/bin/env python3
"""
Comprehensive SMS debugging script
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.sms_service import sms_service
from app.core.config import settings

print("\n" + "="*70)
print("🔍 KisanAI SMS Service Diagnostic")
print("="*70 + "\n")

# 1. Check configuration
print("📋 Configuration:")
print(f"   Account SID: {settings.TWILIO_ACCOUNT_SID}")
print(f"   Auth Token: {settings.TWILIO_AUTH_TOKEN[:10]}...{settings.TWILIO_AUTH_TOKEN[-4:]}")
print(f"   From Number: {settings.TWILIO_PHONE_NUMBER}")
print(f"   To Number: {settings.ADMIN_PHONE_NUMBER}")
print(f"   Service Enabled: {sms_service.is_enabled}")
print()

# 2. Check if service is initialized
if not sms_service.is_enabled:
    print("❌ SMS Service is NOT enabled!")
    print("   Check your .env file configuration")
    sys.exit(1)

print("✅ SMS Service is enabled\n")

# 3. Test SMS sending with detailed error reporting
print("📱 Attempting to send test SMS...")
print()

try:
    from twilio.rest import Client
    from twilio.base.exceptions import TwilioRestException
    
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    
    # Send test message
    message = client.messages.create(
        body="🌾 KisanAI Test - If you receive this, SMS is working perfectly! ✅",
        from_=settings.TWILIO_PHONE_NUMBER,
        to=settings.ADMIN_PHONE_NUMBER
    )
    
    print("✅ SUCCESS! SMS sent successfully!")
    print(f"   Message SID: {message.sid}")
    print(f"   Status: {message.status}")
    print(f"   From: {message.from_}")
    print(f"   To: {message.to}")
    print(f"\n📱 Check your phone: {settings.ADMIN_PHONE_NUMBER}")
    print("\n🎉 Your SMS notification system is working!")
    
except TwilioRestException as e:
    print(f"❌ Twilio API Error!")
    print(f"   Error Code: {e.code}")
    print(f"   Error Message: {e.msg}")
    print()
    
    if e.code == 21608:
        print("🔍 Issue: Unverified Phone Number")
        print("   Solution:")
        print("   1. Go to: https://console.twilio.com/us1/develop/phone-numbers/manage/verified")
        print(f"   2. Add and verify: {settings.ADMIN_PHONE_NUMBER}")
        print("   3. Run this test again")
    elif e.code == 21211:
        print("🔍 Issue: Invalid 'To' Phone Number")
        print(f"   Check that {settings.ADMIN_PHONE_NUMBER} is in correct format")
        print("   Format should be: +917983207219")
    elif e.code == 21606:
        print("🔍 Issue: Invalid 'From' Phone Number")
        print(f"   Check that {settings.TWILIO_PHONE_NUMBER} is correct")
    else:
        print("🔍 Check Twilio logs for more details:")
        print("   https://console.twilio.com/us1/monitor/logs/sms")
    
except Exception as e:
    print(f"❌ Unexpected Error: {e}")
    print(f"   Type: {type(e).__name__}")

print("\n" + "="*70)
