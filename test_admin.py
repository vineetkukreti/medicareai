import requests

BASE_URL = "http://localhost:8000"

def get_admin_token():
    url = f"{BASE_URL}/api/auth/admin/login"
    data = {"email": "admin@gmail.com", "password": "admin"}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print(f"Failed to login as admin: {response.text}")
        return None

def test_admin_stats(token):
    print("\nTesting Admin Stats...")
    url = f"{BASE_URL}/api/admin/stats"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("✅ Stats Endpoint Works")
        print(response.json())
    else:
        print(f"❌ Stats Endpoint Failed: {response.status_code}")
        print(response.text)

def test_admin_users(token):
    print("\nTesting Admin Users...")
    url = f"{BASE_URL}/api/admin/users"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("✅ Users Endpoint Works")
        print(f"Count: {len(response.json())}")
    else:
        print(f"❌ Users Endpoint Failed: {response.status_code}")
        print(response.text)

def test_admin_doctors(token):
    print("\nTesting Admin Doctors...")
    url = f"{BASE_URL}/api/admin/doctors"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("✅ Doctors Endpoint Works")
        print(f"Count: {len(response.json())}")
    else:
        print(f"❌ Doctors Endpoint Failed: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    token = get_admin_token()
    if token:
        test_admin_stats(token)
        test_admin_users(token)
        test_admin_doctors(token)
