# 📧 Gmail SMTP Setup Guide for KisanAI

Complete guide to set up Gmail for sending automated emails from your KisanAI application.

## 🔐 Step 1: Create Gmail App Password

Google requires an "App Password" for applications to send emails via Gmail SMTP. This is different from your regular Gmail password.

### Prerequisites
- Gmail account
- 2-Step Verification must be enabled

### Get Your App Password

1. **Enable 2-Step Verification** (if not already enabled):
   - Go to: https://myaccount.google.com/security
   - Click "2-Step Verification"
   - Follow the setup process

2. **Generate App Password**:
   - Go to: https://myaccount.google.com/apppasswords
   - Sign in if prompted
   - Select app: **Mail**
   - Select device: **Other (Custom name)**
   - Enter name: **KisanAI**
   - Click **Generate**
   - **Copy the 16-character password** (you'll need this for .env file)

> [!IMPORTANT]
> The App Password is shown only once! Copy it immediately.

---

## ⚙️ Step 2: Configure Environment Variables

Update your `backend/.env` file with email credentials:

```bash
cd /home/vineet/Desktop/projects/kisanAI/backend
nano .env  # or use your preferred editor
```

Add these lines (or update if they exist):

```bash
# Email Configuration (Gmail SMTP)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com          # Your Gmail address
SMTP_PASSWORD=abcd efgh ijkl mnop       # The 16-char App Password you just generated
FROM_EMAIL=your-email@gmail.com         # Same as SMTP_USER
FROM_NAME=KisanAI
```

**Example (with fake credentials)**:
```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=vineetkukreti34@gmail.com
SMTP_PASSWORD=abcd efgh ijkl mnop
FROM_EMAIL=vineetkukreti34@gmail.com
FROM_NAME=KisanAI
```

---

## 🧪 Step 3: Test Email Configuration

### Restart Backend Server

The backend needs to reload the new email configuration:

```bash
# Stop current server (Ctrl+C in the terminal)
# Then restart:
cd /home/vineet/Desktop/projects/kisanAI/backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8001
```

**Look for this message on startup:**
```
✅ Email service initialized successfully
```

If you see this, email is not configured:
```
⚠️  WARNING: Email is not configured. Email notifications will be disabled.
```

### Test Email Sending

Create a test script:

```bash
cd /home/vineet/Desktop/projects/kisanAI/backend
source venv/bin/activate
python -c "from app.services.email_service import email_service; email_service.send_test_email('your-email@gmail.com')"
```

Replace `your-email@gmail.com` with your actual email address.

**Expected output:**
```
✅ Email sent successfully to your-email@gmail.com
   Subject: 🌾 KisanAI Email Test
```

**Check your email inbox!** You should receive a test email.

---

## 📱 Step 4: Test Welcome & Login Emails

### Test Welcome Email (Signup)

1. Open your app: http://localhost:5173
2. Go to **Signup** page
3. Create a new account with your email
4. **Check your email** - you should receive a welcome email!

### Test Login Alert Email

1. Go to **Login** page
2. Login with the account you just created
3. **Check your email** - you should receive a login alert email!

---

## 🐛 Troubleshooting

### "SMTP Authentication failed"

**Cause**: Wrong email or App Password

**Solution**:
1. Double-check `SMTP_USER` in .env (must be full Gmail address)
2. Verify `SMTP_PASSWORD` is the 16-character App Password (not regular password)
3. Make sure there are no extra spaces in the password
4. Regenerate App Password if needed

### "Email service not enabled"

**Cause**: Environment variables not loaded

**Solution**:
1. Check `.env` file exists in `backend/` directory
2. Restart backend server
3. Check for typos in variable names

### Emails not received

**Possible causes**:
1. **Check spam folder** - Gmail might mark it as spam initially
2. **Gmail daily limit** - Free Gmail allows ~500 emails/day
3. **Wrong FROM_EMAIL** - Must match SMTP_USER

### "Connection refused" or "Timeout"

**Cause**: Firewall or network issue

**Solution**:
1. Check internet connection
2. Verify port 587 is not blocked
3. Try using port 465 with SSL (update SMTP_PORT in .env)

---

## 📊 Gmail Limits

**Free Gmail Account:**
- **500 emails per day** (rolling 24-hour period)
- **500 recipients per email**
- **99 emails per hour** (approximately)

**For higher volume:**
- Use Google Workspace (paid)
- Or switch to SendGrid, AWS SES, or Mailgun

---

## 🔒 Security Best Practices

1. **Never commit `.env` file** - It's in `.gitignore`
2. **Use App Password** - Never use your regular Gmail password
3. **Rotate passwords** - Change App Password periodically
4. **Monitor usage** - Check Gmail sent folder for unusual activity
5. **Revoke if compromised** - Delete App Password at https://myaccount.google.com/apppasswords

---

## ✅ Verification Checklist

Before going live:

- [ ] 2-Step Verification enabled on Gmail
- [ ] App Password generated
- [ ] `.env` file updated with credentials
- [ ] Backend server restarted
- [ ] Test email sent successfully
- [ ] Welcome email received on signup
- [ ] Login alert email received on login
- [ ] Emails not in spam folder
- [ ] Email templates look professional

---

## 🎉 You're Ready!

Your KisanAI application now sends:
- ✅ **Welcome emails** when users sign up
- ✅ **Login alerts** for account security

**Email Features:**
- Professional HTML templates
- Responsive design
- Security notifications
- Error handling (auth works even if email fails)

For production deployment, see [DEPLOYMENT.md](file:///home/vineet/Desktop/projects/kisanAI/DEPLOYMENT.md).
