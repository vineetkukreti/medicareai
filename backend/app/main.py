from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
from app.modules.auth.router import router as auth_router
from app.modules.contact.router import router as contact_router
from app.modules.chat.router import router as chat_router
from app.modules.dashboard.symptoms_router import router as symptoms_router
from app.modules.medications.router import router as medications_router
from app.modules.appointments.router import router as appointments_router
from app.modules.health_records.router import router as health_records_router
from app.modules.dashboard.router import router as dashboard_router
from app.modules.dashboard.insights_router import router as insights_router
from app.modules.voice_agent.router import router as voice_agent_router
from app.services.rag_service import rag_service

# Import all models to ensure they are registered with Base
from app.modules.auth import models as auth_models
from app.modules.contact import models as contact_models
from app.modules.chat import models as chat_models
from app.modules.health_records import models as health_records_models
from app.modules.medications import models as medications_models
from app.modules.appointments import models as appointments_models
from app.modules.voice_agent import models as voice_agent_models
from app.modules.dashboard import models as dashboard_models

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
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(contact_router, prefix="/api", tags=["Contact"])
# Admin endpoints are now in auth and contact routers
app.include_router(chat_router, prefix="/api", tags=["Chatbot"])
app.include_router(symptoms_router, prefix="/api", tags=["Symptoms"])
app.include_router(medications_router, prefix="/api", tags=["Medications"])
app.include_router(appointments_router, prefix="/api", tags=["Appointments"])
app.include_router(health_records_router, prefix="/api", tags=["Health Records"])
app.include_router(dashboard_router, prefix="/api", tags=["Health Dashboard"])
app.include_router(insights_router, prefix="/api/insights", tags=["Health Insights"])
app.include_router(voice_agent_router, prefix="/api", tags=["Voice Agent"])

@app.get("/")
def read_root():
    return {
        "message": "Welcome to MediCareAI API",
        "version": "2.0.0",
        "description": "Your AI-Powered Health Companion"
    }
