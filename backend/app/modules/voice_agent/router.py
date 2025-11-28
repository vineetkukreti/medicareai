from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.voice_agent import schemas
from app.modules.voice_agent.service import voice_agent_service

router = APIRouter()

@router.post("/voice/session", response_model=schemas.VoiceSessionResponse)
async def create_voice_session(
    request: schemas.VoiceSessionCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new voice session
    """
    return voice_agent_service.create_session(db, request.user_id)

@router.get("/voice/session/{session_id}", response_model=schemas.VoiceSessionResponse)
async def get_voice_session(
    session_id: str,
    db: Session = Depends(get_db)
):
    """
    Get voice session details
    """
    session = voice_agent_service.get_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session
