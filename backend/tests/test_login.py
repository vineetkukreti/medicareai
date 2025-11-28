#!/usr/bin/env python3
"""
Test login authentication for debugging
"""
import sys
sys.path.insert(0, '/home/vineet/Desktop/projects/kisanAI/backend')

from app.core.database import SessionLocal
from app.models import User
from app.core.security import verify_password

def test_login(email, password):
    """Test if login credentials work"""
    db = SessionLocal()
    try:
        # Find user
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            print(f"❌ User not found: {email}")
            return False
        
        print(f"✅ User found: {user.email}")
        print(f"   ID: {user.id}")
        print(f"   Name: {user.full_name}")
        print(f"   Has password: {bool(user.hashed_password)}")
        
        # Test password
        if verify_password(password, user.hashed_password):
            print(f"✅ Password correct!")
            return True
        else:
            print(f"❌ Password incorrect!")
            return False
            
    finally:
        db.close()

def list_users():
    """List all users in database"""
    db = SessionLocal()
    try:
        users = db.query(User).all()
        print(f"\n📋 Total users: {len(users)}\n")
        for user in users:
            print(f"  ID: {user.id}")
            print(f"  Email: {user.email}")
            print(f"  Name: {user.full_name}")
            print(f"  Has password: {bool(user.hashed_password)}")
            print()
    finally:
        db.close()

if __name__ == "__main__":
    print("🔐 Login Authentication Test")
    print("=" * 50)
    
    # List all users
    list_users()
    
    # Test login
    print("\n🧪 Testing Login")
    print("=" * 50)
    
    if len(sys.argv) >= 3:
        email = sys.argv[1]
        password = sys.argv[2]
        test_login(email, password)
    else:
        print("Usage: python test_login.py <email> <password>")
        print("\nExample:")
        print("  python test_login.py user@example.com mypassword")
