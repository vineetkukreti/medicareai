from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas import SymptomCheck, SymptomCheckResponse
from app.services.ai_service import ai_service

router = APIRouter()

@router.post("/symptoms/check", response_model=SymptomCheckResponse)
async def check_symptoms(symptom_data: SymptomCheck, db: Session = Depends(get_db)):
    """
    Analyze symptoms and provide possible conditions and recommendations
    """
    result = await ai_service.analyze_symptoms(
        symptoms=symptom_data.symptoms,
        age=symptom_data.age,
        gender=symptom_data.gender
    )
    
    return SymptomCheckResponse(**result)

@router.get("/health-advice/{topic}")
async def get_health_advice(topic: str):
    """
    Get general health advice on a specific topic
    """
    advice = await ai_service.get_health_advice(topic)
    return {"topic": topic, "advice": advice}
