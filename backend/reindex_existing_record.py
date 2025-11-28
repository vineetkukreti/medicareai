"""
Re-index existing health record with PDF content extraction via API
"""
import requests
import sqlite3

USER_ID = 3
RECORD_ID = 2
BASE_URL = "http://localhost:8000"

# Get record details from database
conn = sqlite3.connect('kisanai.db')
cursor = conn.cursor()
cursor.execute("SELECT title, record_type, record_date, description, file_url FROM health_records WHERE id = ?", (RECORD_ID,))
record = cursor.fetchone()
conn.close()

if not record:
    print(f"❌ Record {RECORD_ID} not found")
    exit(1)

title, record_type, record_date, description, file_url = record
print(f"Found record: {title}")
print(f"File URL: {file_url}")

# Trigger refresh embeddings - this will re-process all records including extracting PDF content
print("\n🔄 Triggering refresh embeddings (this will extract PDF content)...")
response = requests.post(f"{BASE_URL}/api/insights/refresh?user_id={USER_ID}")

if response.status_code == 200:
    print("✅ Refresh started")
    print("\n⏳ Waiting 5 seconds for background processing...")
    import time
    time.sleep(5)
    
    # Test query
    print("\n🔍 Testing query: 'What are my complete lab results with values?'")
    response = requests.post(
        f"{BASE_URL}/api/insights/query?user_id={USER_ID}",
        json={"query": "What are my complete lab results? Give me all the values and parameters tested."},
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        print("\n" + "="*60)
        print("RAG Response:")
        print("="*60)
        print(response.json()['insight'])
        print("="*60)
    else:
        print(f"❌ Query failed: {response.status_code}")
        print(response.text)
else:
    print(f"❌ Refresh failed: {response.status_code}")
    print(response.text)
