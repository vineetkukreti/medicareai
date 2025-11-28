import sys
import os
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Add backend to path to import app modules
sys.path.append(os.getcwd())

from app import models
from app.core.database import engine

Session = sessionmaker(bind=engine)

def clear_data():
    with Session() as db:
        print("🧹 Cleaning up database...")
        # Get admin user
        admin = db.query(models.User).filter(models.User.id == 1).first()
        if admin:
            print(f"ℹ️  Preserving Admin: {admin.email} (ID: {admin.id})")
        else:
            print("⚠️  Warning: Admin user (ID 1) not found!")

        # Delete non-admin users
        deleted_users = db.query(models.User).filter(models.User.id != 1).delete(synchronize_session=False)
        
        # 2. Delete all contact messages
        deleted_contacts = db.query(models.ContactMessage).delete(synchronize_session=False)
        
        db.commit()
        
        print("-" * 30)
        print(f"✅ Deleted {deleted_users} users")
        print(f"✅ Deleted {deleted_contacts} contact messages")
        print("-" * 30)
        print("Database cleanup complete!")

if __name__ == "__main__":
    clear_data()
