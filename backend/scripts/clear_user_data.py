#!/usr/bin/env python3
"""
Clear all data for a specific user (database only)
Run this while the server is running - RAG will be cleared when records are deleted via API
"""
import sys
sys.path.insert(0, '/home/vineet/Desktop/projects/kisanAI/backend')

from app.core.database import SessionLocal
from app.modules.auth.models import User
from app.modules.health_records.models import HealthRecord
from app.modules.medications.models import Medication
from app.modules.appointments.models import Appointment
from app.modules.dashboard.models import HealthProfile, SleepRecord, ActivityRecord, VitalRecord, BodyMeasurement
from app.modules.chat.models import ChatConversation

USER_EMAIL = "vineet.k@palpx.com"

def clear_user_data():
    db = SessionLocal()
    try:
        # Find user
        user = db.query(User).filter(User.email == USER_EMAIL).first()
        
        if not user:
            print(f"❌ User not found: {USER_EMAIL}")
            return
        
        user_id = user.id
        print(f"✅ Found user: {user.email} (ID: {user_id})")
        print(f"   Name: {user.full_name}")
        print()
        
        total_deleted = 0
        
        # Clear Health Records
        health_records = db.query(HealthRecord).filter(HealthRecord.user_id == user_id).all()
        count = len(health_records)
        print(f"🗑️  Deleting {count} health records...")
        for record in health_records:
            db.delete(record)
        total_deleted += count
        
        # Clear Medications
        medications = db.query(Medication).filter(Medication.user_id == user_id).all()
        count = len(medications)
        print(f"🗑️  Deleting {count} medications...")
        for med in medications:
            db.delete(med)
        total_deleted += count
        
        # Clear Appointments
        appointments = db.query(Appointment).filter(Appointment.user_id == user_id).all()
        count = len(appointments)
        print(f"🗑️  Deleting {count} appointments...")
        for appt in appointments:
            db.delete(appt)
        total_deleted += count
        
        # Clear Chat Conversations
        chats = db.query(ChatConversation).filter(ChatConversation.user_id == user_id).all()
        count = len(chats)
        print(f"🗑️  Deleting {count} chat conversations...")
        for chat in chats:
            db.delete(chat)
        total_deleted += count
        
        # Clear Dashboard Data
        health_profile = db.query(HealthProfile).filter(HealthProfile.user_id == user_id).first()
        if health_profile:
            print(f"🗑️  Deleting health profile...")
            db.delete(health_profile)
            total_deleted += 1
        
        sleep_records = db.query(SleepRecord).filter(SleepRecord.user_id == user_id).all()
        count = len(sleep_records)
        print(f"🗑️  Deleting {count} sleep records...")
        for record in sleep_records:
            db.delete(record)
        total_deleted += count
        
        activity_records = db.query(ActivityRecord).filter(ActivityRecord.user_id == user_id).all()
        count = len(activity_records)
        print(f"🗑️  Deleting {count} activity records...")
        for record in activity_records:
            db.delete(record)
        total_deleted += count
        
        vital_records = db.query(VitalRecord).filter(VitalRecord.user_id == user_id).all()
        count = len(vital_records)
        print(f"🗑️  Deleting {count} vital records...")
        for record in vital_records:
            db.delete(record)
        total_deleted += count
        
        body_measurements = db.query(BodyMeasurement).filter(BodyMeasurement.user_id == user_id).all()
        count = len(body_measurements)
        print(f"🗑️  Deleting {count} body measurements...")
        for record in body_measurements:
            db.delete(record)
        total_deleted += count
        
        # Commit database changes
        db.commit()
        print()
        print("=" * 60)
        print(f"✅ DATABASE CLEARED - {total_deleted} records deleted")
        print(f"✅ USER: {USER_EMAIL}")
        print("=" * 60)
        print()
        print("ℹ️  Note: RAG data will be automatically cleaned up when")
        print("   you use the refresh embeddings endpoint in the app.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("=" * 60)
    print(f"CLEARING ALL DATA FOR USER: {USER_EMAIL}")
    print("=" * 60)
    print()
    
    confirm = input("Are you sure you want to delete ALL data for this user? (yes/no): ")
    if confirm.lower() == "yes":
        clear_user_data()
    else:
        print("❌ Operation cancelled")
