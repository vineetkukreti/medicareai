from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
from app.api.endpoints import auth, contact, admin, chatbot, symptoms, medications, appointments, health_records, health_dashboard, profile, health_insights
from app.services.rag_service import rag_service

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="MediCareAI API", version="2.0.0", description="AI-Powered Healthcare Assistant API")

# Initialize Qdrant Collection on Startup
@app.on_event("startup")
async def startup_event():
    try:
        rag_service.initialize_collection()
    except Exception as e:
        print(f"Failed to initialize RAG service: {e}")

# CORS Configuration
origins = [
    "http://localhost:5173",  # Vite default port
    "http://localhost:5174",  # Vite alternate port
    "http://localhost:5175",  # Vite alternate port 2
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(contact.router, prefix="/api", tags=["Contact"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])
app.include_router(chatbot.router, prefix="/api", tags=["Chatbot"])
app.include_router(symptoms.router, prefix="/api", tags=["Symptoms"])
app.include_router(medications.router, prefix="/api", tags=["Medications"])
app.include_router(appointments.router, prefix="/api", tags=["Appointments"])
app.include_router(health_records.router, prefix="/api", tags=["Health Records"])
app.include_router(health_dashboard.router, prefix="/api", tags=["Health Dashboard"])
app.include_router(profile.router, prefix="/api", tags=["Profile"])
app.include_router(health_insights.router, prefix="/api/insights", tags=["Health Insights"])

@app.get("/")
def read_root():
    return {
        "message": "Welcome to MediCareAI API",
        "version": "2.0.0",
        "description": "Your AI-Powered Health Companion"
    }
