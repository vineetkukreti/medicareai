from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.schemas import (
    HealthProfileCreate, HealthProfileResponse,
    SleepRecordResponse, ActivityRecordResponse,
    VitalRecordResponse, BodyMeasurementResponse,
    DashboardSummary
)
from app.models import (
    HealthProfile, SleepRecord, ActivityRecord,
    VitalRecord, BodyMeasurement
)
from app.services.health_parser import AppleHealthParser
from typing import List, Optional
from datetime import datetime, timedelta, date
from app.services.rag_service import rag_service
import tempfile
import os

router = APIRouter()

@router.post("/health/upload")
async def upload_health_data(
    user_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload and parse Apple Health export XML file
    """
    if not file.filename.endswith('.xml'):
        raise HTTPException(status_code=400, detail="Only XML files are supported")
    
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xml') as temp_file:
        content = await file.read()
        temp_file.write(content)
        temp_file_path = temp_file.name
    
    try:
        # Parse the XML file
        parser = AppleHealthParser(temp_file_path)
        parser.parse()
        
        # Extract personal info
        personal_info = parser.get_personal_info()
        height, weight, weight_date = parser.get_height_weight()
        
        # Create or update health profile
        profile = db.query(HealthProfile).filter(HealthProfile.user_id == user_id).first()
        if profile:
            # Update existing profile
            for key, value in personal_info.items():
                if value is not None:
                    setattr(profile, key, value)
            if height:
                profile.height = height
            if weight:
                profile.current_weight = weight
        else:
            # Create new profile
            profile = HealthProfile(
                user_id=user_id,
                height=height,
                current_weight=weight,
                **personal_info
            )
            db.add(profile)
        
        # Extract and save sleep records
        sleep_records = parser.get_sleep_records()
        sleep_count = 0
        for sleep_data in sleep_records:
            # Check if record already exists
            existing = db.query(SleepRecord).filter(
                SleepRecord.user_id == user_id,
                SleepRecord.date == sleep_data['date']
            ).first()
            
            if not existing:
                sleep_record = SleepRecord(user_id=user_id, **sleep_data)
                db.add(sleep_record)
                sleep_count += 1
        
        # Extract and save activity records
        activity_records = parser.get_activity_records()
        activity_count = 0
        for activity_data in activity_records:
            # Check if record already exists
            existing = db.query(ActivityRecord).filter(
                ActivityRecord.user_id == user_id,
                ActivityRecord.date == activity_data['date']
            ).first()
            
            if existing:
                # Update existing record
                for key, value in activity_data.items():
                    if key != 'date':
                        setattr(existing, key, value)
            else:
                activity_record = ActivityRecord(user_id=user_id, **activity_data)
                db.add(activity_record)
                activity_count += 1
        
        # Extract and save vital records
        vital_records = parser.get_vital_records()
        vital_count = 0
        for vital_data in vital_records:
            # Only save if we don't have a record within 1 minute
            existing = db.query(VitalRecord).filter(
                VitalRecord.user_id == user_id,
                VitalRecord.recorded_at >= vital_data['recorded_at'] - timedelta(minutes=1),
                VitalRecord.recorded_at <= vital_data['recorded_at'] + timedelta(minutes=1)
            ).first()
            
            if not existing:
                vital_record = VitalRecord(user_id=user_id, **vital_data)
                db.add(vital_record)
                vital_count += 1
        
        # Save weight measurement if available
        if weight and weight_date:
            existing_weight = db.query(BodyMeasurement).filter(
                BodyMeasurement.user_id == user_id,
                BodyMeasurement.measured_at == weight_date
            ).first()
            
            if not existing_weight:
                weight_record = BodyMeasurement(
                    user_id=user_id,
                    measured_at=weight_date,
                    weight=weight
                )
                db.add(weight_record)
        
        db.commit()
        
        # Trigger RAG ingestion in background
        try:
            # Upsert personal info
            rag_service.upsert_data(
                user_id=user_id,
                data_type="personal_info",
                content=f"Personal Info: {personal_info}, Height: {height}cm, Weight: {weight}kg",
                metadata={"source": "apple_health_export"}
            )
            
            # Upsert sleep summary
            if sleep_records:
                sleep_summary = f"Recent sleep records: {len(sleep_records)} records found. Last record: {sleep_records[-1]['date']} - {sleep_records[-1]['total_duration']} mins"
                rag_service.upsert_data(
                    user_id=user_id,
                    data_type="sleep_records",
                    content=sleep_summary,
                    metadata={"count": len(sleep_records), "last_date": str(sleep_records[-1]['date'])}
                )
                
            # Upsert activity summary
            if activity_records:
                activity_summary = f"Recent activity records: {len(activity_records)} records found. Last record: {activity_records[-1]['date']} - Steps: {activity_records[-1].get('steps', 0)}"
                rag_service.upsert_data(
                    user_id=user_id,
                    data_type="activity_records",
                    content=activity_summary,
                    metadata={"count": len(activity_records), "last_date": str(activity_records[-1]['date'])}
                )
                
        except Exception as e:
            print(f"Error triggering RAG ingestion: {e}")
        
        return {
            "message": "Health data uploaded successfully",
            "summary": {
                "sleep_records": sleep_count,
                "activity_records": activity_count,
                "vital_records": vital_count,
                "profile_updated": True
            }
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error parsing health data: {str(e)}")
    finally:
        # Clean up temp file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@router.get("/health/profile/{user_id}", response_model=HealthProfileResponse)
async def get_health_profile(user_id: int, db: Session = Depends(get_db)):
    """
    Get user's health profile
    """
    profile = db.query(HealthProfile).filter(HealthProfile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Health profile not found")
    return profile

@router.get("/health/sleep/{user_id}", response_model=List[SleepRecordResponse])
async def get_sleep_records(
    user_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """
    Get sleep records for a user
    """
    query = db.query(SleepRecord).filter(SleepRecord.user_id == user_id)
    
    if start_date:
        query = query.filter(SleepRecord.date >= start_date)
    if end_date:
        query = query.filter(SleepRecord.date <= end_date)
    
    records = query.order_by(SleepRecord.date.desc()).all()
    return records

@router.get("/health/activity/{user_id}", response_model=List[ActivityRecordResponse])
async def get_activity_records(
    user_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """
    Get activity records for a user
    """
    query = db.query(ActivityRecord).filter(ActivityRecord.user_id == user_id)
    
    if start_date:
        query = query.filter(ActivityRecord.date >= start_date)
    if end_date:
        query = query.filter(ActivityRecord.date <= end_date)
    
    records = query.order_by(ActivityRecord.date.desc()).all()
    return records

@router.get("/health/vitals/{user_id}", response_model=List[VitalRecordResponse])
async def get_vital_records(
    user_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get vital records for a user
    """
    query = db.query(VitalRecord).filter(VitalRecord.user_id == user_id)
    
    if start_date:
        query = query.filter(VitalRecord.recorded_at >= start_date)
    if end_date:
        query = query.filter(VitalRecord.recorded_at <= end_date)
    
    records = query.order_by(VitalRecord.recorded_at.desc()).limit(limit).all()
    return records

@router.get("/health/dashboard/{user_id}", response_model=DashboardSummary)
async def get_dashboard_summary(user_id: int, db: Session = Depends(get_db)):
    """
    Get comprehensive dashboard summary with today's stats, week trends, and month averages
    """
    # Get profile
    profile = db.query(HealthProfile).filter(HealthProfile.user_id == user_id).first()
    
    today = date.today()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # Today's stats
    today_activity = db.query(ActivityRecord).filter(
        ActivityRecord.user_id == user_id,
        ActivityRecord.date == today
    ).first()
    
    last_night_sleep = db.query(SleepRecord).filter(
        SleepRecord.user_id == user_id,
        SleepRecord.date == today
    ).first()
    
    latest_heart_rate = db.query(VitalRecord).filter(
        VitalRecord.user_id == user_id,
        VitalRecord.heart_rate.isnot(None)
    ).order_by(VitalRecord.recorded_at.desc()).first()
    
    today_stats = {
        "steps": today_activity.steps if today_activity else 0,
        "active_calories": today_activity.active_calories if today_activity else 0,
        "distance": today_activity.distance if today_activity else 0,
        "sleep_duration": last_night_sleep.total_duration if last_night_sleep else 0,
        "heart_rate": latest_heart_rate.heart_rate if latest_heart_rate else None
    }
    
    # Week trends (last 7 days)
    week_activities = db.query(ActivityRecord).filter(
        ActivityRecord.user_id == user_id,
        ActivityRecord.date >= week_ago,
        ActivityRecord.date <= today
    ).all()
    
    week_sleep = db.query(SleepRecord).filter(
        SleepRecord.user_id == user_id,
        SleepRecord.date >= week_ago,
        SleepRecord.date <= today
    ).all()
    
    week_trends = {
        "daily_steps": [{"date": str(a.date), "steps": a.steps} for a in week_activities],
        "daily_sleep": [{"date": str(s.date), "duration": s.total_duration} for s in week_sleep],
        "total_steps": sum(a.steps for a in week_activities),
        "avg_sleep": sum(s.total_duration for s in week_sleep) / len(week_sleep) if week_sleep else 0
    }
    
    # Month averages (last 30 days)
    month_activities = db.query(ActivityRecord).filter(
        ActivityRecord.user_id == user_id,
        ActivityRecord.date >= month_ago,
        ActivityRecord.date <= today
    ).all()
    
    month_sleep = db.query(SleepRecord).filter(
        SleepRecord.user_id == user_id,
        SleepRecord.date >= month_ago,
        SleepRecord.date <= today
    ).all()
    
    month_heart_rate = db.query(func.avg(VitalRecord.heart_rate)).filter(
        VitalRecord.user_id == user_id,
        VitalRecord.recorded_at >= datetime.combine(month_ago, datetime.min.time()),
        VitalRecord.heart_rate.isnot(None)
    ).scalar()
    
    month_averages = {
        "avg_steps": int(sum(a.steps for a in month_activities) / len(month_activities)) if month_activities else 0,
        "avg_sleep": int(sum(s.total_duration for s in month_sleep) / len(month_sleep)) if month_sleep else 0,
        "avg_heart_rate": int(month_heart_rate) if month_heart_rate else None,
        "total_distance": sum(a.distance for a in month_activities)
    }
    
    return DashboardSummary(
        profile=HealthProfileResponse.from_orm(profile) if profile else None,
        today_stats=today_stats,
        week_trends=week_trends,
        month_averages=month_averages
    )
