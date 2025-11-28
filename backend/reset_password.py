"""
Reset password for a user
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

from app.core.database import SessionLocal
from app.models import User
from app.core.security import get_password_hash

EMAIL = "vineetkukreti34@gmail.com"
NEW_PASSWORD = "vineetkukreti34@gmail.com"

db = SessionLocal()

try:
    user = db.query(User).filter(User.email == EMAIL).first()
    if user:
        user.hashed_password = get_password_hash(NEW_PASSWORD)
        db.commit()
        print(f"✅ Password reset successfully for {EMAIL}")
        print(f"   New password: {NEW_PASSWORD}")
    else:
        print(f"❌ User {EMAIL} not found")
finally:
    db.close()
