# 🔧 MediCareAI Services Setup Guide

## 📧 Email Service Setup (Gmail)

### Step 1: Enable 2-Factor Authentication
1. Go to your Google Account: https://myaccount.google.com/
2. Navigate to **Security** → **2-Step Verification**
3. Enable 2-Step Verification if not already enabled

### Step 2: Generate App Password
1. Go to: https://myaccount.google.com/apppasswords
2. Select **App**: Mail
3. Select **Device**: Other (Custom name) → Enter "MediCareAI"
4. Click **Generate**
5. Copy the 16-character password (remove spaces)

### Step 3: Update .env File
```bash
SMTP_USER=your-actual-gmail@gmail.com
SMTP_PASSWORD=your-16-char-app-password
FROM_EMAIL=your-actual-gmail@gmail.com
FROM_NAME=MediCareAI
```

### Step 4: Test Email Service
```bash
cd /home/vineet/Desktop/projects/kisanAI/backend
python test_email.py
```

---

## 📱 SMS Service Setup (Twilio)

### Step 1: Create Twilio Account
1. Sign up at: https://www.twilio.com/try-twilio
2. Verify your phone number
3. You'll get **$15 free credit** for testing

### Step 2: Get Credentials
1. Go to Twilio Console: https://console.twilio.com/
2. Find your **Account SID** and **Auth Token** on the dashboard
3. Get a Twilio phone number:
   - Go to **Phone Numbers** → **Manage** → **Buy a number**
   - Choose a number (free with trial credit)

### Step 3: Update .env File
```bash
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+1234567890  # Your Twilio number
ADMIN_PHONE_NUMBER=+917983207219  # Your personal number (already set)
```

### Step 4: Verify Phone Number (Trial Account)
- Twilio trial accounts can only send to **verified numbers**
- Go to: https://console.twilio.com/us1/develop/phone-numbers/manage/verified
- Add your phone number (+917983207219)

### Step 5: Test SMS Service
```bash
cd /home/vineet/Desktop/projects/kisanAI/backend
python test_sms.py
```

---

## 🚀 Quick Setup Options

### Option 1: Email Only (Recommended for Testing)
If you just want to test email notifications:
1. Set up Gmail App Password (Steps above)
2. Update `.env` with your Gmail credentials
3. Leave Twilio settings as placeholders
4. Restart the backend server

### Option 2: SMS Only
If you just want to test SMS:
1. Set up Twilio account (Steps above)
2. Update `.env` with Twilio credentials
3. Leave email settings as placeholders
4. Restart the backend server

### Option 3: Both Services
Set up both email and SMS for full functionality.

---

## 🧪 Testing Your Setup

After updating `.env`, restart the backend:
```bash
# Stop current server (Ctrl+C)
# Then restart
cd /home/vineet/Desktop/projects/kisanAI
./start.sh
```

Or run individual test scripts:
```bash
# Test email
python backend/test_email.py

# Test SMS
python backend/test_sms.py
```

---

## ⚠️ Important Notes

### For Email:
- **Must use Gmail App Password**, not your regular Gmail password
- Regular password will NOT work
- App passwords are 16 characters without spaces

### For Twilio Trial:
- Free $15 credit included
- Can only send to verified phone numbers
- Messages will have "Sent from a Twilio trial account" prefix
- Upgrade to paid account to remove restrictions

### Security:
- Never commit `.env` file to git (already in .gitignore)
- Keep your credentials secure
- Change SECRET_KEY in production

---

## 🆘 Troubleshooting

### Email not working?
- Check if 2FA is enabled on Google account
- Verify you're using App Password, not regular password
- Check SMTP_USER matches FROM_EMAIL
- Look for error messages in backend logs

### SMS not working?
- Verify phone number is verified in Twilio console (for trial)
- Check Account SID and Auth Token are correct
- Ensure phone numbers include country code (+1 for US, +91 for India)
- Check Twilio console for error messages

### Still having issues?
Run the test scripts to see detailed error messages:
```bash
python backend/test_email.py
python backend/test_sms.py
```
