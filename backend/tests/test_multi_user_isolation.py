"""
Comprehensive Multi-User Data Isolation Test

This test verifies that the RAG system strictly isolates data between users
and prevents any cross-patient information leakage.

Test Scenarios:
1. Two users with distinct appointments
2. Verify User A only sees their own data
3. Verify User B only sees their own data
4. Verify AI responses don't leak cross-user information
5. Test empty data scenario
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

# Test users with distinct data
USER_A = {
    "email": "patient_a@test.com",
    "password": "securepass123",
    "full_name": "Patient A",
    "appointment": {
        "doctor_name": "Dr. Lisa Anderson",
        "specialty": "General Medicine",
        "reason": "fever consultation",
        "appointment_date": "2025-11-30T05:34:00"
    }
}

USER_B = {
    "email": "patient_b@test.com",
    "password": "securepass456",
    "full_name": "Patient B",
    "appointment": {
        "doctor_name": "Dr. Smith",
        "specialty": "Cardiology",
        "reason": "annual checkup",
        "appointment_date": "2025-12-15T10:00:00"
    }
}

def signup(user_data):
    """Create a new user account"""
    response = requests.post(
        f"{BASE_URL}/api/auth/signup",
        json={
            "email": user_data["email"],
            "password": user_data["password"],
            "full_name": user_data["full_name"]
        }
    )
    return response.status_code == 200

def login(email, password):
    """Login and get JWT token"""
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={"email": email, "password": password}
    )
    if response.status_code == 200:
        return response.json()['token']
    return None

def create_appointment(token, appointment_data):
    """Create an appointment for the authenticated user"""
    response = requests.post(
        f"{BASE_URL}/api/appointments",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        },
        json=appointment_data
    )
    return response.status_code == 200

def refresh_embeddings(token):
    """Trigger RAG embedding refresh"""
    response = requests.post(
        f"{BASE_URL}/api/insights/refresh",
        headers={"Authorization": f"Bearer {token}"}
    )
    return response.status_code == 200

def query_rag(token, query):
    """Query the RAG system"""
    response = requests.post(
        f"{BASE_URL}/api/insights/query",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        },
        json={"query": query}
    )
    if response.status_code == 200:
        return response.json()['insight']
    return None

def check_data_leakage(response_text, forbidden_terms):
    """Check if response contains any forbidden terms"""
    response_lower = response_text.lower()
    leaked_terms = [term for term in forbidden_terms if term.lower() in response_lower]
    return leaked_terms


if __name__ == "__main__":
    print("=" * 80)
    print("MULTI-USER DATA ISOLATION TEST")
    print("=" * 80)

    # Test 1: Setup User A
    print("\n📋 Test 1: Setting up User A")
    print("-" * 80)
    signup(USER_A)
    token_a = login(USER_A["email"], USER_A["password"])
    if not token_a:
        print("❌ Failed to login as User A")
        exit(1)

    if create_appointment(token_a, USER_A["appointment"]):
        print(f"✅ Created appointment for User A: {USER_A['appointment']['doctor_name']}")
    else:
        print("❌ Failed to create appointment for User A")

    # Refresh embeddings
    if refresh_embeddings(token_a):
        print("✅ Triggered embedding refresh for User A")
        time.sleep(2)  # Wait for background task
    else:
        print("⚠️  Failed to refresh embeddings for User A")

    # Test 2: Setup User B
    print("\n📋 Test 2: Setting up User B")
    print("-" * 80)
    signup(USER_B)
    token_b = login(USER_B["email"], USER_B["password"])
    if not token_b:
        print("❌ Failed to login as User B")
        exit(1)

    if create_appointment(token_b, USER_B["appointment"]):
        print(f"✅ Created appointment for User B: {USER_B['appointment']['doctor_name']}")
    else:
        print("❌ Failed to create appointment for User B")

    # Refresh embeddings
    if refresh_embeddings(token_b):
        print("✅ Triggered embedding refresh for User B")
        time.sleep(2)  # Wait for background task
    else:
        print("⚠️  Failed to refresh embeddings for User B")

    # Test 3: User A queries for appointments
    print("\n🔍 Test 3: User A queries for appointments")
    print("-" * 80)
    query = "Show my upcoming appointments"
    response_a = query_rag(token_a, query)

    if response_a:
        print("✅ User A received response")
        
        # Check for User A's data (should be present)
        if "Lisa Anderson" in response_a or "General Medicine" in response_a:
            print("✅ Response contains User A's appointment (Dr. Lisa Anderson)")
        else:
            print("⚠️  Response doesn't mention User A's appointment")
        
        # Check for User B's data (should NOT be present)
        leaked_terms = check_data_leakage(response_a, ["Dr. Smith", "Cardiology", "annual checkup"])
        if leaked_terms:
            print(f"❌ DATA LEAKAGE DETECTED! User A's response contains User B's data: {leaked_terms}")
            print(f"Response preview: {response_a[:200]}")
        else:
            print("✅ No data leakage - User B's data not present in User A's response")
    else:
        print("❌ Failed to get response for User A")

    # Test 4: User B queries for appointments
    print("\n🔍 Test 4: User B queries for appointments")
    print("-" * 80)
    response_b = query_rag(token_b, query)

    if response_b:
        print("✅ User B received response")
        
        # Check for User B's data (should be present)
        if "Dr. Smith" in response_b or "Cardiology" in response_b:
            print("✅ Response contains User B's appointment (Dr. Smith)")
        else:
            print("⚠️  Response doesn't mention User B's appointment")
        
        # Check for User A's data (should NOT be present)
        leaked_terms = check_data_leakage(response_b, ["Lisa Anderson", "General Medicine", "fever"])
        if leaked_terms:
            print(f"❌ DATA LEAKAGE DETECTED! User B's response contains User A's data: {leaked_terms}")
            print(f"Response preview: {response_b[:200]}")
        else:
            print("✅ No data leakage - User A's data not present in User B's response")
    else:
        print("❌ Failed to get response for User B")

    # Test 5: Empty data scenario (new user)
    print("\n🔍 Test 5: New user with no data")
    print("-" * 80)
    USER_C = {"email": "patient_c@test.com", "password": "pass789", "full_name": "Patient C"}
    signup(USER_C)
    token_c = login(USER_C["email"], USER_C["password"])

    if token_c:
        response_c = query_rag(token_c, "What are my appointments?")
        if response_c:
            print("✅ User C (no data) received response")
            
            # Check for proper empty data handling
            if "don't have enough" in response_c.lower() or "no data" in response_c.lower() or "no appointments" in response_c.lower():
                print("✅ Response properly indicates no data available")
            else:
                print("⚠️  Response doesn't clearly indicate no data")
            
            # Check for data leakage from other users
            leaked_terms = check_data_leakage(response_c, ["Lisa Anderson", "Dr. Smith", "Cardiology", "General Medicine"])
            if leaked_terms:
                print(f"❌ DATA LEAKAGE DETECTED! User C's response contains other users' data: {leaked_terms}")
            else:
                print("✅ No data leakage - Other users' data not present")
        else:
            print("❌ Failed to get response for User C")

    # Final Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print("✅ User A and User B created with distinct appointments")
    print("✅ Each user's RAG queries tested")
    print("✅ Cross-user data leakage checked")
    print("✅ Empty data scenario tested")
    print("\n🔒 SECURITY VERIFICATION COMPLETE")
    print("=" * 80)
