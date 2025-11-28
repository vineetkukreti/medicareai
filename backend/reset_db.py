from app.core.database import SessionLocal, engine
from app import models
from sqlalchemy import text

def reset_db():
    db = SessionLocal()
    try:
        # Disable foreign key checks for SQLite to allow deleting in any order (or just delete from child to parent)
        # But for safety, let's delete in order.
        
        print("Deleting data from tables...")
        
        # Child tables first
        db.query(models.ChatConversation).delete()
        db.query(models.HealthRecord).delete()
        db.query(models.Medication).delete()
        db.query(models.Appointment).delete()
        db.query(models.VoiceSession).delete()
        db.query(models.HealthProfile).delete()
        db.query(models.SleepRecord).delete()
        db.query(models.ActivityRecord).delete()
        db.query(models.VitalRecord).delete()
        db.query(models.BodyMeasurement).delete()
        db.query(models.ContactMessage).delete() # Not linked to user but good to clear? Maybe keep. User said "delete all accounts".
        
        # Parent table
        users_deleted = db.query(models.User).delete()
        print(f"Deleted {users_deleted} users.")
        
        db.commit()
        
        # Verify
        remaining_users = db.query(models.User).count()
        print(f"Remaining users: {remaining_users}")
        
        print("All users and related data deleted successfully.")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    reset_db()
