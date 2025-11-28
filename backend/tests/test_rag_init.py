"""
Script to initialize Qdrant collection and test RAG with sample data
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from app.services.rag_service import rag_service
import requests

def main():
    print("🚀 Initializing Qdrant Collection...")
    try:
        rag_service.initialize_collection()
        print("✅ Collection initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        return
    
    # Add some test data for user 2
    print("\n📝 Adding test data for user 2...")
    user_id = 2
    
    test_data = [
        ("medication", "Medication: Aspirin, Dosage: 100mg, Frequency: Daily, Start Date: 2024-01-01, Notes: Take with food"),
        ("appointment", "Appointment: Dr. Smith (Cardiology), Date: 2025-12-15 10:00:00, Reason: Annual checkup"),
        ("health_record", "Health Record: Blood Test Results (Lab), Date: 2024-11-15, Description: All values within normal range. Cholesterol: 180mg/dL, Blood Sugar: 95mg/dL"),
        ("personal_info", "Personal Info: DOB: 1990-06-12, Sex: Male, Blood Type: O+, Height: 175cm, Weight: 70kg"),
    ]
    
    for data_type, content in test_data:
        try:
            rag_service.upsert_data(user_id, data_type, content, {"test": True})
            print(f"✅ Added {data_type}")
        except Exception as e:
            print(f"❌ Failed to add {data_type}: {e}")
    
    # Test search
    print("\n🔍 Testing search...")
    query = "What medications am I taking?"
    try:
        results = rag_service.search(user_id, query, limit=5)
        print(f"Found {len(results)} results:")
        for i, result in enumerate(results, 1):
            print(f"  {i}. {result['content'][:100]}... (score: {result['score']:.3f})")
    except Exception as e:
        print(f"❌ Search failed: {e}")
    
    # Test insight generation
    print("\n💡 Testing insight generation...")
    try:
        insight = rag_service.generate_insight(user_id, query)
        print(f"Insight:\n{insight}")
    except Exception as e:
        print(f"❌ Insight generation failed: {e}")
    
    # Test API endpoint
    print("\n🌐 Testing API endpoint...")
    try:
        response = requests.post(
            "http://localhost:8000/api/insights/query?user_id=2",
            json={"query": "What are my recent health metrics?"}
        )
        if response.status_code == 200:
            print(f"✅ API Response: {response.json()['insight'][:200]}...")
        else:
            print(f"❌ API returned {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ API call failed: {e}")

if __name__ == "__main__":
    main()
