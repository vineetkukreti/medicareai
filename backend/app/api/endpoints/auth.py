from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.core.database import get_db
from app.core.security import create_access_token, get_password_hash, verify_password, ACCESS_TOKEN_EXPIRE_MINUTES
from app import models, schemas
from app.services.email_service import email_service
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/signup", response_model=schemas.User)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Create new user account and send welcome email."""
    # Check if email already exists
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=400, 
            detail="This email is already registered. Please log in instead or use a different email."
        )
    
    # Create user
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, full_name=user.full_name, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    logger.info(f"👤 New user registered: {user.email}")
    
    # Send welcome email
    try:
        email_sent = email_service.send_welcome_email(
            user_name=user.full_name or user.email.split('@')[0],
            user_email=user.email
        )
        
        if email_sent:
            logger.info(f"📧 Welcome email sent to {user.email}")
        else:
            logger.warning(f"⚠️  Welcome email failed for {user.email}")
    except Exception as e:
        # Don't fail signup if email fails
        logger.error(f"❌ Error sending welcome email: {e}")
    
    return db_user

@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Authenticate user and send login alert email."""
    # First check if user exists
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account not found. Please check your email or sign up for a new account.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Then verify password
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password. Please try again.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    logger.info(f"🔐 User logged in: {user.email}")
    
    # Send login alert email
    try:
        email_sent = email_service.send_login_alert_email(
            user_name=user.full_name or user.email.split('@')[0],
            user_email=user.email
        )
        
        if email_sent:
            logger.info(f"📧 Login alert email sent to {user.email}")
        else:
            logger.warning(f"⚠️  Login alert email failed for {user.email}")
    except Exception as e:
        # Don't fail login if email fails
        logger.error(f"❌ Error sending login alert email: {e}")
    
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "email": user.email,
        "full_name": user.full_name
    }
