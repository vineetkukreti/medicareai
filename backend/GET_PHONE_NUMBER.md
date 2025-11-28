# 📱 Get Your Twilio Phone Number - Quick Guide

## ✅ Current Status

- **Account SID**: ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx ✅
- **Auth Token**: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx ✅
- **Phone Number**: ❌ **NEED TO GET THIS**

---

## 🚀 Steps to Get a Free Twilio Phone Number

### Step 1: Go to Phone Numbers Page

Click this link: [Get Twilio Phone Number](https://console.twilio.com/us1/develop/phone-numbers/manage/search)

Or navigate manually:
1. Go to https://console.twilio.com/
2. Click **Phone Numbers** in the left sidebar
3. Click **Manage** → **Buy a number**

### Step 2: Search for a Number

1. **Select Country**: 
   - Try **India** first (if available for trial)
   - Or select **United States** (always available)

2. **Capabilities** (make sure these are checked):
   - ✅ SMS
   - ✅ MMS (optional)
   - ✅ Voice (optional)

3. Click **Search**

### Step 3: Buy a Number (FREE with Trial)

1. You'll see a list of available numbers
2. Click **Buy** on any number you like
3. Confirm the purchase (it's FREE with your trial credit)
4. **Copy the phone number** (format: `+1234567890`)

### Step 4: Update Your Configuration

Once you have the number, update the `.env` file:

```bash
cd /home/vineet/Desktop/projects/kisanAI/backend
nano .env  # or use your preferred editor
```

Change this line:
```bash
TWILIO_PHONE_NUMBER=+1234567890  # Replace with your actual number
```

**Example:**
```bash
TWILIO_PHONE_NUMBER=+12025551234  # If you got a US number
```

### Step 5: Verify Your Phone Number (Important!)

For the **free trial**, you can only send SMS to **verified numbers**.

1. Go to: https://console.twilio.com/us1/develop/phone-numbers/manage/verified
2. Click **Add a new number**
3. Enter: **+917983207219**
4. Choose verification method: **SMS** or **Call**
5. Enter the verification code you receive
6. Click **Verify**

---

## 🧪 Test Your Setup

After completing all steps above:

### 1. Restart Backend Server

Stop the current server (Ctrl+C in the terminal) and restart:

```bash
cd /home/vineet/Desktop/projects/kisanAI/backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

**Look for this message:**
```
✅ Twilio SMS service initialized successfully
```

### 2. Run Test Script

```bash
cd /home/vineet/Desktop/projects/kisanAI/backend
source venv/bin/activate
python test_sms.py
```

### 3. Check Your Phone

You should receive a test SMS on **+917983207219** within seconds!

---

## 🐛 Troubleshooting

### "You don't have any Twilio phone numbers"
- You need to buy a number first (Step 2-3 above)
- It's FREE with trial credit

### "Permission denied" or "Unverified number"
- Verify +917983207219 in Twilio Console (Step 5)
- Free trial can only send to verified numbers

### "Invalid phone number format"
- Phone numbers must include country code
- Format: `+917983207219` ✅
- Format: `7983207219` ❌

---

## 💡 Quick Summary

1. ✅ Get Twilio phone number (FREE)
2. ✅ Verify your phone (+917983207219)
3. ✅ Update `.env` with the Twilio number
4. ✅ Restart backend
5. ✅ Run `python test_sms.py`
6. ✅ Receive SMS!

**Need help?** Let me know which step you're stuck on!
