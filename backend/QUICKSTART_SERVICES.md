# 🚀 Quick Start: Enable Email & SMS Services

## ⚡ The Problem
Your Email and SMS services are showing as **disabled** because the `.env` file has placeholder values.

## ✅ Quick Solutions

### Option 1: Interactive Setup (Easiest)
```bash
cd /home/vineet/Desktop/projects/kisanAI/backend
python configure_services.py
```
This will guide you through the setup step-by-step.

---

### Option 2: Manual Setup

#### 📧 Email (Gmail) - 5 Minutes
1. **Get Gmail App Password:**
   - Visit: https://myaccount.google.com/apppasswords
   - Create password for "MediCareAI"
   - Copy the 16-character password

2. **Edit `.env` file:**
   ```bash
   nano /home/vineet/Desktop/projects/kisanAI/backend/.env
   ```

3. **Update these lines:**
   ```env
   SMTP_USER=your-actual-email@gmail.com
   SMTP_PASSWORD=abcd efgh ijkl mnop  # Your 16-char app password
   FROM_EMAIL=your-actual-email@gmail.com
   ```

4. **Test it:**
   ```bash
   python test_email.py
   ```

---

#### 📱 SMS (Twilio) - 10 Minutes
1. **Sign up for Twilio:**
   - Visit: https://www.twilio.com/try-twilio
   - Get $15 free credit

2. **Get credentials:**
   - Dashboard: https://console.twilio.com/
   - Copy **Account SID** and **Auth Token**
   - Get a phone number (free with trial)

3. **Verify your phone (IMPORTANT for trial):**
   - Visit: https://console.twilio.com/us1/develop/phone-numbers/manage/verified
   - Add: +917983207219

4. **Edit `.env` file:**
   ```bash
   nano /home/vineet/Desktop/projects/kisanAI/backend/.env
   ```

5. **Update these lines:**
   ```env
   TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   TWILIO_AUTH_TOKEN=your_auth_token_here
   TWILIO_PHONE_NUMBER=+1234567890  # Your Twilio number
   ```

6. **Test it:**
   ```bash
   python test_sms.py
   ```

---

### Option 3: Email Only (Recommended for Quick Testing)
Just set up email (easier and free):
1. Follow "Email Setup" above
2. Leave Twilio settings as-is
3. Restart backend

---

## 🔄 After Configuration

**Restart the backend server:**
```bash
# Stop current server (Ctrl+C in the terminal running ./start.sh)
# Then restart:
cd /home/vineet/Desktop/projects/kisanAI
./start.sh
```

You should see:
- ✅ Email service initialized successfully
- ✅ Twilio SMS service initialized successfully

Instead of:
- ⚠️ Email notifications disabled
- ⚠️ SMS notifications disabled

---

## 🧪 Test Scripts

```bash
# Test email service
python backend/test_email.py

# Test SMS service
python backend/test_sms.py

# Interactive configuration
python backend/configure_services.py
```

---

## 📚 Detailed Documentation
See `SETUP_SERVICES.md` for complete instructions and troubleshooting.

---

## 💡 Recommendations

**For Development/Testing:**
- ✅ Set up Email only (easier, free, no phone verification needed)
- ⏭️ Skip SMS for now

**For Production:**
- ✅ Set up both Email and SMS
- ✅ Upgrade Twilio to paid account (removes "trial" prefix)

---

## ❓ Need Help?

Run the test scripts - they show detailed error messages:
```bash
python backend/test_email.py
python backend/test_sms.py
```
