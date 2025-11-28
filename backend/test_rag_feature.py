import os
import sys
from dotenv import load_dotenv

# Add backend directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

from app.services.rag_service import rag_service

def test_rag():
    print("Testing RAG Service...")
    
    # 1. Initialize Collection
    print("\n1. Initializing Collection...")
    try:
        rag_service.initialize_collection()
        print("✅ Collection initialized")
    except Exception as e:
        print(f"❌ Failed to initialize collection: {e}")
        return

    # 2. Upsert Test Data
    print("\n2. Upserting Test Data...")
    user_id = 999 # Test user
    test_data = [
        ("personal_info", "Patient is a 30-year-old male, 180cm, 75kg. No known allergies."),
        ("medication", "Taking Vitamin D 1000IU daily."),
        ("sleep_records", "Average sleep duration: 7 hours. Deep sleep: 1.5 hours."),
        ("appointment", "Upcoming appointment with Dr. Smith (Cardiology) on 2025-12-01.")
    ]
    
    try:
        for data_type, content in test_data:
            rag_service.upsert_data(
                user_id=user_id,
                data_type=data_type,
                content=content,
                metadata={"test": True}
            )
        print("✅ Test data upserted")
    except Exception as e:
        print(f"❌ Failed to upsert data: {e}")
        return

    # 3. Search
    print("\n3. Searching...")
    query = "What medications am I taking?"
    try:
        results = rag_service.search(user_id, query)
        print(f"Found {len(results)} results")
        for res in results:
            print(f"- {res['content']} (Score: {res['score']})")
        
        if len(results) > 0:
            print("✅ Search successful")
        else:
            print("❌ Search failed (no results)")
    except Exception as e:
        print(f"❌ Failed to search: {e}")
        return

    # 4. Generate Insight
    print("\n4. Generating Insight...")
    query = "Summarize my health profile and upcoming appointments."
    try:
        insight = rag_service.generate_insight(user_id, query)
        print(f"Insight:\n{insight}")
        print("✅ Insight generation successful")
    except Exception as e:
        print(f"❌ Failed to generate insight: {e}")
        return

if __name__ == "__main__":
    test_rag()
