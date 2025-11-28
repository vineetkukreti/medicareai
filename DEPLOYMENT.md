# KisanAI Deployment Guide

Complete guide to deploying KisanAI to production with SMS notifications.

## 📋 Prerequisites

- Twilio account (free trial available)
- Git repository (GitHub, GitLab, etc.)
- Domain name (optional but recommended)

---

## 🔧 Step 1: Twilio Setup

### Create Twilio Account

1. **Sign up** at https://www.twilio.com/try-twilio
2. **Verify your email** and complete registration
3. **Get a free phone number** from the Twilio Console

### Get Your Credentials

1. Go to **Twilio Console Dashboard**: https://console.twilio.com/
2. Find your credentials:
   - **Account SID**: `ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` (from your Twilio Console)
   - **Auth Token**: Click "Show" to reveal (keep this secret!)
   - **Phone Number**: Your Twilio phone number (format: +1234567890)

### Verify Your Phone Number (Free Trial)

> [!IMPORTANT]
> Twilio free trial can only send SMS to **verified numbers**.

1. Go to **Phone Numbers** → **Verified Caller IDs**
2. Click **Add a new number**
3. Enter your phone number: **+917983207219**
4. Complete verification via SMS or call

---

## ⚙️ Step 2: Configure Environment Variables

### Update Backend `.env` File

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Edit the `.env` file with your actual Twilio credentials:
   ```bash
   # Twilio SMS Configuration
   TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   TWILIO_AUTH_TOKEN=your_actual_auth_token_here
   TWILIO_PHONE_NUMBER=+1234567890  # Your Twilio number
   
   # Admin Contact
   ADMIN_PHONE_NUMBER=+1234567890
   
   # Database (use PostgreSQL for production)
   DATABASE_URL=sqlite:///./kisanai.db
   
   # Security (generate a strong random key)
   SECRET_KEY=your-super-secret-key-here
   
   # App Settings
   APP_NAME=KisanAI
   DEBUG=False
   ```

3. **Generate a secure SECRET_KEY**:
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

---

## 🧪 Step 3: Test Locally

### Start Backend

```bash
cd backend
source venv/bin/activate  # Activate virtual environment
uvicorn app.main:app --reload
```

You should see:
```
⚠️  WARNING: Twilio is not configured...  # If credentials not set
✅ Twilio SMS service initialized successfully  # If configured correctly
```

### Start Frontend

```bash
cd frontend
npm run dev
```

### Test SMS Notification

1. Open http://localhost:5173 in your browser
2. Navigate to the **Contact** page
3. Fill out the contact form:
   - Name: Test User
   - Email: test@example.com
   - Message: Testing SMS notifications!
4. Submit the form
5. **Check your phone** (+917983207219) for SMS notification

Expected SMS format:
```
🌾 KisanAI - New Contact Form Submission

Name: Test User
Email: test@example.com

Message:
Testing SMS notifications!

---
Reply to contact them directly.
```

---

## 🚀 Step 4: Production Deployment

### Option A: Railway.app (Recommended - Easiest)

**Why Railway?**
- Free tier available ($5 credit/month)
- Auto-deploy from Git
- Built-in PostgreSQL database
- Easy environment variable management

**Steps:**

1. **Sign up** at https://railway.app
2. **Create New Project** → **Deploy from GitHub**
3. **Connect your repository**
4. **Add PostgreSQL database**:
   - Click "New" → "Database" → "PostgreSQL"
   - Railway will auto-generate `DATABASE_URL`
5. **Configure environment variables**:
   - Go to your service → "Variables"
   - Add all variables from `.env` file
6. **Deploy**:
   - Railway auto-deploys on every Git push
   - Get your public URL (e.g., `kisanai.up.railway.app`)

### Option B: Render.com (Free Tier)

1. **Sign up** at https://render.com
2. **Create Web Service**:
   - Connect GitHub repository
   - Build Command: `cd backend && pip install -r requirements.txt`
   - Start Command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
3. **Add PostgreSQL database** (free tier)
4. **Set environment variables** in dashboard
5. **Deploy frontend** as Static Site:
   - Build Command: `cd frontend && npm install && npm run build`
   - Publish Directory: `frontend/dist`

### Option C: DigitalOcean App Platform

1. **Sign up** at https://www.digitalocean.com
2. **Create App** → **GitHub**
3. **Configure components**:
   - Backend: Python app
   - Frontend: Static site
   - Database: PostgreSQL
4. **Set environment variables**
5. **Deploy**

### Option D: Self-Hosted (VPS)

For AWS, GCP, Azure, or your own server:

1. **Set up server** (Ubuntu recommended)
2. **Install dependencies**:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip nodejs npm postgresql nginx
   ```
3. **Clone repository**
4. **Set up PostgreSQL database**
5. **Configure Nginx** as reverse proxy
6. **Use systemd** to run backend as service
7. **Set up SSL** with Let's Encrypt

---

## 🗄️ Step 5: Database Migration (Production)

### Switch from SQLite to PostgreSQL

**Why PostgreSQL?**
- Better performance for concurrent users
- Required by most cloud platforms
- More reliable for production

**Update DATABASE_URL:**
```bash
# Format:
DATABASE_URL=postgresql://username:password@host:port/database

# Example (Railway auto-generates this):
DATABASE_URL=postgresql://postgres:password@containers-us-west-123.railway.app:5432/railway
```

---

## 🔒 Security Best Practices

### 1. Environment Variables
- ✅ Never commit `.env` to Git
- ✅ Use different credentials for dev/staging/prod
- ✅ Rotate secrets regularly

### 2. HTTPS
- ✅ Always use HTTPS in production
- ✅ Most platforms (Railway, Render) provide free SSL

### 3. CORS Configuration
Update `backend/app/main.py` with your production domain:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Update this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 4. Rate Limiting
Add rate limiting to prevent spam:
```bash
pip install slowapi
```

---

## 📊 Monitoring & Maintenance

### Twilio Dashboard
- Monitor SMS delivery: https://console.twilio.com/us1/monitor/logs/sms
- Check usage and costs
- View delivery status

### Application Logs
Check backend logs for SMS notifications:
```
✅ SMS sent successfully! SID: SM...
📱 SMS notification sent to admin successfully
❌ Twilio API error: [error details]
```

### Cost Management

**Twilio Pricing (as of 2024):**
- Free trial: $15 credit
- SMS (India): ~$0.0075 per message
- SMS (US): ~$0.0079 per message

**Estimate:**
- 100 contacts/month = ~$0.75
- 1,000 contacts/month = ~$7.50

---

## 🌍 Custom Domain Setup

### 1. Purchase Domain
- Namecheap, GoDaddy, Google Domains, etc.

### 2. Configure DNS
Point your domain to deployment platform:

**Railway:**
```
CNAME: www.yourdomain.com → your-app.up.railway.app
```

**Render:**
```
CNAME: www.yourdomain.com → your-app.onrender.com
```

### 3. Update CORS
Update allowed origins in backend to include your domain.

---

## 🐛 Troubleshooting

### SMS Not Sending

**Check 1: Twilio Configuration**
```bash
# Backend logs should show:
✅ Twilio SMS service initialized successfully

# If you see this, credentials are wrong:
⚠️  WARNING: Twilio is not configured
```

**Check 2: Phone Number Format**
- Must include country code: `+917983207219` ✅
- Without country code: `7983207219` ❌

**Check 3: Free Trial Restrictions**
- Verify recipient number in Twilio Console
- Upgrade account to send to unverified numbers

**Check 4: Twilio Logs**
- Check https://console.twilio.com/us1/monitor/logs/sms
- Look for error messages

### Database Connection Issues

**SQLite (Development):**
- File permissions issue
- Check `kisanai.db` exists in backend directory

**PostgreSQL (Production):**
- Verify `DATABASE_URL` format
- Check database is running
- Verify network connectivity

### CORS Errors

Update `allow_origins` in `backend/app/main.py`:
```python
allow_origins=[
    "http://localhost:5173",  # Development
    "https://yourdomain.com",  # Production
]
```

---

## 📈 Scaling for Global Users

### 1. Multi-Region Deployment
- Deploy to multiple regions (US, EU, Asia)
- Use CDN for frontend assets

### 2. Database Optimization
- Add indexes on frequently queried fields
- Use connection pooling
- Consider read replicas

### 3. Caching
- Add Redis for session management
- Cache API responses

### 4. Email Notifications (Alternative)
For high volume, consider email instead of SMS:
- **SendGrid**: 100 emails/day free
- **AWS SES**: $0.10 per 1,000 emails
- More cost-effective than SMS

### 5. Multi-Language Support
Add i18n for global audience:
- Hindi, English, regional languages
- Use `react-i18next` for frontend

---

## ✅ Production Checklist

Before going live:

- [ ] Twilio account created and verified
- [ ] Environment variables configured
- [ ] SMS notifications tested locally
- [ ] Database migrated to PostgreSQL
- [ ] HTTPS enabled
- [ ] CORS configured for production domain
- [ ] Error monitoring set up (Sentry recommended)
- [ ] Backup strategy implemented
- [ ] Rate limiting added
- [ ] Custom domain configured (optional)
- [ ] Analytics added (Google Analytics)
- [ ] Legal pages added (Privacy Policy, Terms of Service)

---

## 🆘 Support

### Twilio Support
- Documentation: https://www.twilio.com/docs
- Support: https://support.twilio.com

### Platform Support
- Railway: https://railway.app/help
- Render: https://render.com/docs
- DigitalOcean: https://www.digitalocean.com/community

---

## 🎉 Next Steps

Once deployed:

1. **Test thoroughly** with real contact form submissions
2. **Monitor SMS delivery** in Twilio dashboard
3. **Gather user feedback**
4. **Iterate and improve**

**Your KisanAI application is now ready to serve users globally! 🌾**
