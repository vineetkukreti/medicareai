from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.core.database import get_db, SessionLocal
from app.core.security import get_current_user
from app.modules.auth.models import User
from app.modules.dashboard.service import dashboard_service
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class InsightQuery(BaseModel):
    query: str

class InsightResponse(BaseModel):
    insight: str

@router.post("/query", response_model=InsightResponse)
async def get_health_insight(
    query: InsightQuery,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get personalized health insights based on authenticated user's data.
    """
    try:
        insight = dashboard_service.generate_insight(current_user.id, query.query)
        return {"insight": insight}
    except Exception as e:
        logger.error(f"Error generating insight for user {current_user.id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/refresh")
async def refresh_embeddings(
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Trigger a background task to refresh authenticated user's embeddings.
    """
    background_tasks.add_task(process_refresh_embeddings_task, current_user.id)
    return {"message": "Embedding refresh started in background"}

def process_refresh_embeddings_task(user_id: int):
    db = SessionLocal()
    try:
        dashboard_service.process_refresh_embeddings(user_id, db)
    finally:
        db.close()
