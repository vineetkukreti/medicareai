"""
Inspect what's actually in Qdrant for user 3
"""
import requests

USER_ID = 3
BASE_URL = "http://localhost:8000"

# Create a debug endpoint to inspect Qdrant contents
query = """
Tell me everything you know about my health. Include all my records, medications, appointments, and any other information you have about me.
"""

print(f"Querying RAG for all data about user {USER_ID}...")

response = requests.post(
    f"{BASE_URL}/api/insights/query?user_id={USER_ID}",
    json={"query": query},
    headers={"Content-Type": "application/json"}
)

if response.status_code == 200:
    data = response.json()
    print("\n" + "="*60)
    print("RAG Response:")
    print("="*60)
    print(data.get('insight'))
else:
    print(f"Error: {response.status_code}")
    print(response.text)
