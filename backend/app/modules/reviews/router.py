from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user, oauth2_scheme
from app.modules.auth.models import User
from app.modules.reviews import schemas
from app.modules.reviews.service import review_service
from app.services.notification_service import notification_service
import asyncio

router = APIRouter()

@router.post("/", response_model=schemas.ReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_review(
    review_data: schemas.ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new review for a doctor after an appointment.
    """
    review = review_service.create_review(db, review_data, current_user.id)
    
    # Get patient name for response
    patient_name = current_user.full_name
    
    response = schemas.ReviewResponse(
        id=review.id,
        patient_id=review.patient_id,
        patient_name=patient_name,
        doctor_id=review.doctor_id,
        appointment_id=review.appointment_id,
        rating=review.rating,
        comment=review.comment,
        created_at=review.created_at
    )
    
    # Send SSE notification to doctor
    await notification_service.send_notification(
        doctor_id=review.doctor_id,
        event_type="new_review",
        data={
            "review_id": review.id,
            "patient_name": patient_name,
            "rating": review.rating,
            "comment": review.comment,
            "created_at": review.created_at.isoformat()
        }
    )
    
    return response


@router.get("/doctors/{doctor_id}", response_model=List[schemas.ReviewResponse])
def get_doctor_reviews(
    doctor_id: int,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """
    Get all reviews for a specific doctor (paginated).
    """
    reviews = review_service.get_doctor_reviews(db, doctor_id, skip, limit)
    return reviews

@router.get("/my-reviews", response_model=List[schemas.ReviewResponse])
def get_my_reviews(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    """
    Get reviews for the currently authenticated doctor.
    """
    from app.modules.doctors.models import Doctor
    from app.core.security import verify_token
    
    # Verify token and get email
    try:
        payload = verify_token(token)
        email = payload.get("sub")
        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
    except HTTPException:
        raise
    
    # Check if current user is a doctor
    doctor = db.query(Doctor).filter(Doctor.email == email).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized as a doctor"
        )
    
    reviews = review_service.get_doctor_reviews(db, doctor.id, skip, limit)
    return reviews

@router.get("/doctors/{doctor_id}/summary", response_model=schemas.DoctorRatingSummary)
def get_doctor_rating_summary(
    doctor_id: int,
    db: Session = Depends(get_db)
):
    """
    Get aggregated rating statistics for a doctor.
    """
    return review_service.get_doctor_rating_summary(db, doctor_id)

@router.get("/appointments/{appointment_id}/check", response_model=schemas.ReviewExistsResponse)
def check_review_exists(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Check if a review exists for a specific appointment.
    """
    review = review_service.check_review_exists(db, appointment_id, current_user.id)
    
    if review:
        return schemas.ReviewExistsResponse(
            exists=True,
            review=schemas.ReviewResponse(
                id=review.id,
                patient_id=review.patient_id,
                patient_name=current_user.full_name,
                doctor_id=review.doctor_id,
                appointment_id=review.appointment_id,
                rating=review.rating,
                comment=review.comment,
                created_at=review.created_at
            )
        )
    
    return schemas.ReviewExistsResponse(exists=False, review=None)
