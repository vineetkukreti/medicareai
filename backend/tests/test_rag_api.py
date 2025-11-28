import requests
import json

BASE_URL = "http://localhost:8000"

def test_rag_api():
    print("Testing RAG API...")
    
    # 1. Check Root
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Server is running")
        else:
            print(f"❌ Server returned {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Failed to connect to server: {e}")
        return

    # 2. Test Insight Query
    print("\n2. Testing Insight Query...")
    user_id = 2 # Assuming user 2 exists from previous context
    query = "What is my recent sleep pattern?"
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/insights/query?user_id={user_id}",
            json={"query": query}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Insight received:")
            print(data['insight'])
        else:
            print(f"❌ Failed to get insight: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Error during API call: {e}")

if __name__ == "__main__":
    test_rag_api()
