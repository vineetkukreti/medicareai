"""
Test RAG functionality for a specific user
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

from app.services.rag_service import rag_service
from app.core.database import SessionLocal
from app.models import User, HealthRecord

# User to test
TEST_EMAIL = "vineet.k@palpx.com"

def main():
    db = SessionLocal()
    
    # Get user
    user = db.query(User).filter(User.email == TEST_EMAIL).first()
    if not user:
        print(f"❌ User {TEST_EMAIL} not found!")
        return
    
    print(f"✅ Found user: {user.email} (ID: {user.id})")
    
    # Check health records
    records = db.query(HealthRecord).filter(HealthRecord.user_id == user.id).all()
    print(f"\n📋 User has {len(records)} health records:")
    for record in records:
        print(f"  - {record.title} ({record.record_type}) - {record.record_date}")
        print(f"    Description: {record.description[:100]}...")
    
    # Test search
    print("\n🔍 Testing RAG search...")
    query = "What are my lab results?"
    try:
        results = rag_service.search(user.id, query, limit=10)
        print(f"Found {len(results)} results:")
        for i, result in enumerate(results, 1):
            print(f"\n  Result {i} (score: {result['score']:.3f}):")
            print(f"    Type: {result['metadata'].get('data_type')}")
            print(f"    Content: {result['content'][:150]}...")
    except Exception as e:
        print(f"❌ Search failed: {e}")
    
    # Test insight generation
    print("\n💡 Testing insight generation...")
    try:
        insight = rag_service.generate_insight(user.id, query)
        print(f"Insight:\n{insight}")
    except Exception as e:
        print(f"❌ Insight generation failed: {e}")
    
    db.close()

if __name__ == "__main__":
    main()
