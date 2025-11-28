from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.core.database import get_db
from app.modules.auth import schemas
from app.modules.auth.service import auth_service
from app.services.email_service import email_service
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/signup", response_model=schemas.User)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Create new user account and send welcome email."""
    # Check if email already exists
    if auth_service.get_user_by_email(db, user.email):
        raise HTTPException(
            status_code=400, 
            detail="This email is already registered. Please log in instead or use a different email."
        )
    
    # Create user
    db_user = auth_service.create_user(db, user)
    
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
    user = auth_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token_data = auth_service.create_token(user)
    
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
    
    return token_data

@router.get("/profile/{user_id}", response_model=schemas.UserProfileResponse)
async def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    """
    Get user profile information
    """
    user = auth_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/profile/{user_id}", response_model=schemas.UserProfileResponse)
async def update_user_profile(
    user_id: int,
    profile_data: schemas.UserProfileUpdate,
    db: Session = Depends(get_db)
):
    """
    Update user profile information
    """
    user = auth_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    updated_user = auth_service.update_user_profile(db, user, profile_data)
    return updated_user
