import sys
import os
import unittest
from unittest.mock import MagicMock, patch
from datetime import date, datetime

# Add backend directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.api.endpoints.health_insights import process_refresh_embeddings
from app.models import User, Appointment, Medication, HealthRecord, SleepRecord, ActivityRecord, HealthProfile

class TestRAGIntegration(unittest.TestCase):
    @patch('app.api.endpoints.health_insights.SessionLocal')
    @patch('app.api.endpoints.health_insights.rag_service')
    def test_process_refresh_embeddings(self, mock_rag_service, mock_session_local):
        print("Testing process_refresh_embeddings...")
        # Setup mock DB session
        mock_db = MagicMock()
        mock_session_local.return_value = mock_db
        
        user_id = 1
        
        # Mock data
        mock_profile = HealthProfile(
            user_id=user_id, date_of_birth=date(1990, 1, 1), 
            biological_sex="Male", blood_type="O+", height=180, current_weight=75
        )
        mock_appointment = Appointment(
            id=1, user_id=user_id, doctor_name="Smith", specialty="Cardiology",
            appointment_date=datetime(2025, 1, 1, 10, 0), reason="Checkup"
        )
        mock_medication = Medication(
            id=1, user_id=user_id, medication_name="Aspirin", dosage="100mg",
            frequency="Daily", start_date=date(2024, 1, 1), notes="Take with food", is_active=True
        )
        mock_record = HealthRecord(
            id=1, user_id=user_id, title="Lab Report", record_type="Lab",
            record_date=date(2024, 12, 1), description="Normal"
        )
        
        # Configure mock DB queries
        def side_effect(model):
            query = MagicMock()
            if model == HealthProfile:
                query.filter.return_value.first.return_value = mock_profile
            elif model == Appointment:
                query.filter.return_value.all.return_value = [mock_appointment]
            elif model == Medication:
                query.filter.return_value.filter.return_value.all.return_value = [mock_medication]
                # Handle the double filter for medications
                query.filter.return_value.all.return_value = [mock_medication]
            elif model == HealthRecord:
                query.filter.return_value.all.return_value = [mock_record]
            elif model == SleepRecord:
                query.filter.return_value.order_by.return_value.limit.return_value.all.return_value = []
            elif model == ActivityRecord:
                query.filter.return_value.order_by.return_value.limit.return_value.all.return_value = []
            return query
            
        mock_db.query.side_effect = side_effect
        
        # Run function
        process_refresh_embeddings(user_id)
        
        # Verify calls
        # 1. Personal Info
        mock_rag_service.upsert_data.assert_any_call(
            user_id, "personal_info", 
            "Personal Info: DOB: 1990-01-01, Sex: Male, Blood Type: O+, Height: 180cm, Weight: 75kg", 
            {"source": "health_profile"}
        )
        
        # 2. Appointment
        mock_rag_service.upsert_data.assert_any_call(
            user_id, "appointment",
            "Appointment: Dr. Smith (Cardiology), Date: 2025-01-01 10:00:00, Reason: Checkup",
            {"appointment_id": 1}
        )
        
        # 3. Medication
        mock_rag_service.upsert_data.assert_any_call(
            user_id, "medication",
            "Medication: Aspirin, Dosage: 100mg, Frequency: Daily, Start Date: 2024-01-01, Notes: Take with food",
            {"medication_id": 1}
        )
        
        # 4. Health Record
        mock_rag_service.upsert_data.assert_any_call(
            user_id, "health_record",
            "Health Record: Lab Report (Lab), Date: 2024-12-01, Description: Normal",
            {"record_id": 1}
        )
        
        print("✅ All RAG upsert calls verified successfully")

if __name__ == '__main__':
    unittest.main()
