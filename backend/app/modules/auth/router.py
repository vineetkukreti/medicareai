from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.core.database import get_db
from app.core.security import get_current_user
from app.modules.auth import schemas
from app.modules.auth.models import User
from app.modules.auth.service import auth_service
from app.services.email_service import email_service
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/signup", response_model=schemas.User)
def signup(user: schemas.UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """Create new user account and send welcome email in background."""
    # Check if email already exists
    if auth_service.get_user_by_email(db, user.email):
        raise HTTPException(
            status_code=400, 
            detail="This email is already registered. Please log in instead or use a different email."
        )
    
    # Create user
    db_user = auth_service.create_user(db, user)
    
    logger.info(f"👤 New user registered: {user.email}")
    
    # Send welcome email in background
    background_tasks.add_task(
        email_service.send_welcome_email,
        user_name=user.full_name or user.email.split('@')[0],
        user_email=user.email
    )
    
    return db_user

@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), background_tasks: BackgroundTasks = None, db: Session = Depends(get_db)):
    """Authenticate user and send login alert email in background."""
    user = auth_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token_data = auth_service.create_token(user)
    
    logger.info(f"🔐 User logged in: {user.email}")
    
    # Send login alert email in background
    if background_tasks:
        background_tasks.add_task(
            email_service.send_login_alert_email,
            user_name=user.full_name or user.email.split('@')[0],
            user_email=user.email
        )
    
    return token_data

@router.get("/profile", response_model=schemas.UserProfileResponse)
async def get_user_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Get user profile information for authenticated user
    """
    return current_user

@router.put("/profile", response_model=schemas.UserProfileResponse)
async def update_user_profile(
    profile_data: schemas.UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update user profile information for authenticated user
    """
    updated_user = auth_service.update_user_profile(db, current_user, profile_data)
    return updated_user
