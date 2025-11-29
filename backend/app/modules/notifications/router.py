from fastapi import APIRouter, Depends, Request, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_token
from app.modules.doctors.models import Doctor
from app.services.notification_service import notification_service
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/stream")
async def notification_stream(
    request: Request,
    token: str,
    db: Session = Depends(get_db)
):
    """
    Server-Sent Events endpoint for real-time notifications.
    Doctors connect to this endpoint to receive notifications about new reviews.
    Token is passed as a query parameter since EventSource doesn't support headers.
    """
    try:
        # Verify token and get user email
        payload = verify_token(token)
        email = payload.get("sub")
        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        # Get doctor from database
        doctor = db.query(Doctor).filter(Doctor.email == email).first()
        if not doctor:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized as a doctor"
            )
        
        async def event_generator():
            try:
                async for notification in notification_service.subscribe(doctor.id):
                    # Check if client is still connected
                    if await request.is_disconnected():
                        logger.info(f"📡 Client disconnected for doctor {doctor.id}")
                        break
                    
                    # Format SSE message
                    event = notification.get("event", "message")
                    data = notification.get("data", "{}")
                    
                    yield f"event: {event}\n"
                    yield f"data: {data}\n\n"
            except Exception as e:
                logger.error(f"📡 Error in SSE stream for doctor {doctor.id}: {e}")
        
        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no"  # Disable nginx buffering
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"📡 Error setting up SSE stream: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to establish notification stream"
        )
