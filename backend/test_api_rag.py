"""
Test RAG through the running API server
"""
import requests
import json

BASE_URL = "http://localhost:8000"
USER_ID = 3  # vineet.k@palpx.com

def test_api_health():
    """Test if API is running"""
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ API server is running")
            return True
        else:
            print(f"❌ API returned {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API server not reachable: {e}")
        return False

def test_rag_query():
    """Test RAG query endpoint"""
    query = "What are my lab results?"
    print(f"\n🔍 Testing RAG query: '{query}'")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/insights/query?user_id={USER_ID}",
            json={"query": query},
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Response received:")
            print(f"Insight: {data.get('insight', 'No insight')}")
        else:
            print(f"❌ Error response:")
            print(response.text)
    except Exception as e:
        print(f"❌ Request failed: {e}")

def test_refresh_embeddings():
    """Test refresh embeddings endpoint"""
    print(f"\n🔄 Testing refresh embeddings for user {USER_ID}...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/insights/refresh?user_id={USER_ID}",
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Response: {data}")
        else:
            print(f"❌ Error response:")
            print(response.text)
    except Exception as e:
        print(f"❌ Request failed: {e}")

def main():
    print("=" * 60)
    print("Testing RAG System for user vineet.k@palpx.com (ID: 3)")
    print("=" * 60)
    
    if not test_api_health():
        print("\n❌ API server is not running. Please start it first.")
        return
    
    # First, try to refresh embeddings
    test_refresh_embeddings()
    
    # Wait a moment for background task
    import time
    print("\n⏳ Waiting 3 seconds for embeddings to refresh...")
    time.sleep(3)
    
    # Then test query
    test_rag_query()
    
    # Test another query
    query = "What medications am I taking?"
    print(f"\n🔍 Testing another query: '{query}'")
    try:
        response = requests.post(
            f"{BASE_URL}/api/insights/query?user_id={USER_ID}",
            json={"query": query},
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Response: {data.get('insight')[:200]}...")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Failed: {e}")

if __name__ == "__main__":
    main()
