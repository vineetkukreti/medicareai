# MediCareAI 🏥

Your AI-Powered Health Companion - A comprehensive healthcare assistance application with FastAPI backend and React + Vite frontend.

## ✨ Features

- 💬 **AI Medical Chatbot** - 24/7 intelligent health assistant powered by Google Gemini AI
- 🔍 **Symptom Checker** - AI-powered symptom analysis and health recommendations
- 💊 **Medication Tracker** - Smart medication reminders and tracking
- 📋 **Health Records** - Secure storage for medical records and documents
- 📅 **Appointment Booking** - Schedule and manage healthcare appointments
- 📊 **Health Insights** - Personalized health tips and wellness advice
- 👤 **User Authentication** - Secure signup and login system
- 📱 **SMS & Email Notifications** - Real-time alerts for important updates
- 🔐 **Admin Dashboard** - Manage users and monitor system activity

## 🚀 Technology Stack

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **SQLAlchemy** - SQL toolkit and ORM
- **Google Gemini AI** - Advanced AI for medical chatbot and symptom analysis
- **Twilio** - SMS notifications
- **Python 3.13+**

### Frontend
- **React** - UI library
- **Vite** - Next generation frontend tooling
- **React Router** - Client-side routing
- **Tailwind CSS** - Utility-first CSS framework

## 📋 Requirements

- Python 3.13+
- Node.js 16+ and npm
- Google Gemini API key (for AI features)
- Twilio account (optional, for SMS notifications)
- Gmail account (optional, for email notifications)

## 🛠️ Setup and Installation

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your API keys and credentials

# Run the backend server
uvicorn app.main:app --reload
```

Backend runs at: **http://localhost:8000**

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run the development server
npm run dev
```

Frontend runs at: **http://localhost:5173**

## 🔑 Environment Configuration

### Required API Keys

1. **Google Gemini API Key** (Required for AI features)
   - Get your key from: https://makersuite.google.com/app/apikey
   - Add to `.env`: `GEMINI_API_KEY=your_key_here`

2. **Twilio** (Optional, for SMS notifications)
   - Sign up at: https://www.twilio.com/try-twilio
   - Add credentials to `.env`

3. **Gmail SMTP** (Optional, for email notifications)
   - Get App Password from: https://myaccount.google.com/apppasswords
   - Add credentials to `.env`

### Environment Variables

Copy `backend/.env.example` to `backend/.env` and fill in your values:

```env
# AI Service
GEMINI_API_KEY=your_gemini_api_key_here

# Twilio (Optional)
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890

# Email (Optional)
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=your-email@gmail.com
FROM_NAME=MediCareAI

# Database
DATABASE_URL=sqlite:///./medicareai.db

# Security
SECRET_KEY=your-secret-key-here
```

## 📚 API Documentation

Once the backend is running, visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## 🎯 Key Features Explained

### 1. AI Medical Chatbot
- Powered by Google Gemini AI
- 24/7 availability
- Context-aware conversations
- Medical knowledge base
- Session management

### 2. Symptom Checker
- AI-driven symptom analysis
- Severity assessment
- Possible condition identification
- Personalized recommendations
- Emergency detection

### 3. Medication Tracker
- Add and manage medications
- Dosage tracking
- Frequency reminders
- Notes and special instructions

### 4. Health Records
- Secure document storage
- Lab results management
- Prescription tracking
- Medical history

### 5. Appointment Booking
- Schedule doctor appointments
- Appointment reminders
- Status tracking
- Calendar integration

## 🔒 Security Features

- JWT-based authentication
- Password hashing with bcrypt
- CORS protection
- Input validation
- SQL injection prevention
- XSS protection

## ⚠️ Important Disclaimer

**MediCareAI is an AI-powered health information tool and NOT a replacement for professional medical advice, diagnosis, or treatment.**

- Always consult qualified healthcare professionals for medical decisions
- In case of medical emergencies, call emergency services immediately
- This application provides general health information only
- AI responses should not be considered as medical diagnoses

## 🚀 Deployment

For production deployment:

1. **Database**: Migrate from SQLite to PostgreSQL
2. **Environment**: Set `DEBUG=False` in production
3. **HTTPS**: Use SSL/TLS certificates
4. **Hosting**: Deploy on platforms like:
   - Railway
   - Render
   - DigitalOcean
   - AWS/GCP/Azure

See `DEPLOYMENT.md` for detailed deployment instructions.

## 📝 Project Structure

```
medicareai/
├── backend/
│   ├── app/
│   │   ├── api/endpoints/
│   │   │   ├── auth.py
│   │   │   ├── chatbot.py
│   │   │   ├── symptoms.py
│   │   │   ├── medications.py
│   │   │   ├── appointments.py
│   │   │   └── health_records.py
│   │   ├── services/
│   │   │   ├── ai_service.py
│   │   │   └── email_service.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── main.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── LandingPage.jsx
│   │   │   ├── ChatBot.jsx
│   │   │   ├── SymptomChecker.jsx
│   │   │   ├── MedicationTracker.jsx
│   │   │   └── ...
│   │   └── App.jsx
│   └── package.json
└── README.md
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
- Open an issue on GitHub
- Contact: support@medicareai.com

## 🙏 Acknowledgments

- Google Gemini AI for powering our intelligent features
- Healthcare AI companies for inspiration
- Open source community

---

**Made with ❤️ for better healthcare accessibility**
