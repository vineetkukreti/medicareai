#!/bin/bash
# Script to restart backend with new configuration

echo "🔄 Restarting KisanAI backend with SMS notifications..."
echo ""
echo "⚠️  Make sure you've configured your Twilio credentials in .env file!"
echo "   And verified your admin phone number in Twilio Console:"
echo "   https://console.twilio.com/us1/develop/phone-numbers/manage/verified"
echo ""
echo "Starting server..."
echo ""

cd "$(dirname "$0")"
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
