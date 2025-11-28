"""
Test the new JSON-based RAG response format
"""
import requests
import json

BASE_URL = "http://localhost:8000"
USER_EMAIL = "vineet.k@palpx.com"
USER_PASSWORD = "vineet.k@palpx.com"

def login():
    response = requests.post(f"{BASE_URL}/api/auth/login", json={"email": USER_EMAIL, "password": USER_PASSWORD})
    if response.status_code == 200:
        return response.json()['token']
    return None

def test_query(token):
    print("\n🔍 Testing query: 'What are my lab results?'")
    response = requests.post(
        f"{BASE_URL}/api/insights/query",
        headers={"Authorization": f"Bearer {token}"},
        json={"query": "What are my lab results?"}
    )
    
    if response.status_code == 200:
        data = response.json()
        insight = data['insight']
        print("\n✅ Received Response:")
        try:
            # Try parsing as JSON to verify structure
            parsed = json.loads(insight)
            print(json.dumps(parsed, indent=2))
            print("\n✅ Valid JSON format received!")
        except json.JSONDecodeError:
            print("❌ Response is NOT valid JSON:")
            print(insight)
    else:
        print(f"❌ Query failed: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    token = login()
    if token:
        test_query(token)
    else:
        print("❌ Login failed")
