import requests

BASE_URL = "http://localhost:8000"

def test_admin_login():
    print("Testing Admin Login...")
    url = f"{BASE_URL}/api/auth/admin/login"
    data = {
        "email": "admin@gmail.com",
        "password": "admin"
    }
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("✅ Admin Login Successful")
            print(response.json())
        else:
            print(f"❌ Admin Login Failed: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Admin Login Error: {e}")

def test_user_signup_and_login():
    print("\nTesting User Signup and Login...")
    # Signup
    signup_url = f"{BASE_URL}/api/auth/signup"
    user_data = {
        "email": "testuser_debug@example.com",
        "password": "password123",
        "full_name": "Test User Debug"
    }
    
    # Check if user exists or just try signup
    response = requests.post(signup_url, json=user_data)
    if response.status_code == 200:
        print("✅ Signup Successful")
    elif response.status_code == 400 and "already registered" in response.text:
        print("ℹ️ User already exists, proceeding to login")
    else:
        print(f"❌ Signup Failed: {response.status_code}")
        print(response.text)
        return

    # Login
    login_url = f"{BASE_URL}/api/auth/login"
    login_data = {
        "username": "testuser_debug@example.com",
        "password": "password123"
    }
    response = requests.post(login_url, data=login_data)
    if response.status_code == 200:
        print("✅ User Login Successful")
        print(response.json())
    else:
        print(f"❌ User Login Failed: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    test_admin_login()
    test_user_signup_and_login()
