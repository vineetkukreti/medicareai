from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from app.modules.reviews.models import DoctorReview
from app.modules.reviews import schemas
from app.modules.auth.models import User
from app.modules.appointments.models import Appointment
from fastapi import HTTPException, status

class ReviewService:
    def create_review(
        self, 
        db: Session, 
        review_data: schemas.ReviewCreate, 
        patient_id: int
    ) -> DoctorReview:
        # Verify appointment exists and belongs to patient
        appointment = db.query(Appointment).filter(
            Appointment.id == review_data.appointment_id,
            Appointment.user_id == patient_id
        ).first()
        
        if not appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Appointment not found or does not belong to you"
            )
        
        # Verify appointment is for the specified doctor
        if appointment.doctor_id != review_data.doctor_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Appointment is not with this doctor"
            )
        
        # Check if review already exists
        existing_review = db.query(DoctorReview).filter(
            DoctorReview.patient_id == patient_id,
            DoctorReview.appointment_id == review_data.appointment_id
        ).first()
        
        if existing_review:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You have already reviewed this appointment"
            )
        
        # Create review
        review = DoctorReview(
            patient_id=patient_id,
            doctor_id=review_data.doctor_id,
            appointment_id=review_data.appointment_id,
            rating=review_data.rating,
            comment=review_data.comment
        )
        
        db.add(review)
        db.commit()
        db.refresh(review)
        return review

    def get_doctor_reviews(
        self, 
        db: Session, 
        doctor_id: int, 
        skip: int = 0, 
        limit: int = 20
    ) -> List[dict]:
        reviews = db.query(DoctorReview, User.full_name).join(
            User, DoctorReview.patient_id == User.id
        ).filter(
            DoctorReview.doctor_id == doctor_id
        ).order_by(
            DoctorReview.created_at.desc()
        ).offset(skip).limit(limit).all()
        
        return [
            {
                "id": review.id,
                "patient_id": review.patient_id,
                "patient_name": patient_name or "Anonymous",
                "doctor_id": review.doctor_id,
                "appointment_id": review.appointment_id,
                "rating": review.rating,
                "comment": review.comment,
                "created_at": review.created_at
            }
            for review, patient_name in reviews
        ]

    def get_doctor_rating_summary(
        self, 
        db: Session, 
        doctor_id: int
    ) -> schemas.DoctorRatingSummary:
        reviews = db.query(DoctorReview).filter(
            DoctorReview.doctor_id == doctor_id
        ).all()
        
        if not reviews:
            return schemas.DoctorRatingSummary(
                average_rating=0.0,
                total_reviews=0,
                rating_distribution={1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
            )
        
        total_reviews = len(reviews)
        average_rating = sum(r.rating for r in reviews) / total_reviews
        
        # Calculate distribution
        distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for review in reviews:
            distribution[review.rating] += 1
        
        return schemas.DoctorRatingSummary(
            average_rating=round(average_rating, 2),
            total_reviews=total_reviews,
            rating_distribution=distribution
        )

    def check_review_exists(
        self, 
        db: Session, 
        appointment_id: int, 
        patient_id: int
    ) -> Optional[DoctorReview]:
        return db.query(DoctorReview).filter(
            DoctorReview.appointment_id == appointment_id,
            DoctorReview.patient_id == patient_id
        ).first()

review_service = ReviewService()
