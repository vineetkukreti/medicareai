from app.modules.auth.schemas import (
    UserBase, UserCreate, User, UserResponse, 
    UserProfileUpdate, UserProfileResponse, Token, AdminLoginRequest
)
from app.modules.contact.schemas import (
    ContactCreate, Contact, ContactResponse, AdminReplyRequest
)
from app.modules.chat.schemas import ChatMessage, ChatResponse
from app.modules.health_records.schemas import HealthRecordCreate, HealthRecordResponse
from app.modules.medications.schemas import MedicationCreate, MedicationResponse
from app.modules.appointments.schemas import (
    AppointmentCreate, AppointmentResponse, DoctorScheduleCreate, 
    DoctorScheduleResponse, AvailableSlot
)
from app.modules.voice_agent.schemas import (
    VoiceSessionCreate, VoiceSessionResponse, VoiceAgentMessage, VoiceBookingRequest
)
from app.modules.dashboard.schemas import (
    HealthProfileCreate, HealthProfileResponse, SleepRecordResponse, 
    ActivityRecordResponse, VitalRecordResponse, BodyMeasurementResponse, 
    DashboardSummary, SymptomCheck, SymptomCheckResponse
)
