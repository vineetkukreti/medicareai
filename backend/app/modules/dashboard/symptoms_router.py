from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.dashboard import schemas
from app.modules.dashboard.service import dashboard_service

router = APIRouter()

@router.post("/symptoms/check", response_model=schemas.SymptomCheckResponse)
async def check_symptoms(symptom_data: schemas.SymptomCheck, db: Session = Depends(get_db)):
    """
    Analyze symptoms and provide possible conditions and recommendations
    """
    result = await dashboard_service.analyze_symptoms(
        symptoms=symptom_data.symptoms,
        age=symptom_data.age,
        gender=symptom_data.gender
    )
    
    return schemas.SymptomCheckResponse(**result)

@router.get("/health-advice/{topic}")
async def get_health_advice(topic: str):
    """
    Get general health advice on a specific topic
    """
    advice = await dashboard_service.get_health_advice(topic)
    return {"topic": topic, "advice": advice}
