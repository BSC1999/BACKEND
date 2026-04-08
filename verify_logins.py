import requests
import json

base_url = "http://127.0.0.1:8000/api/auth/login/"
password = "Saveetha_Dental"

users = [
    "admin_777",
    "doctor_111",
    "consultant_222",
    "assistant_333",
    "testdoctor"
]

print("Starting Login Verification...")
print("-" * 30)

for username in users:
    try:
        response = requests.post(
            base_url,
            json={"username": username, "password": password},
            timeout=5
        )
        if response.status_code == 200:
            print(f"[SUCCESS] {username} logged in successfully.")
            # Optional: Check if we can access /api/users/me/ with the token
            token = response.json().get("access")
            me_response = requests.get(
                "http://127.0.0.1:8000/api/users/me/",
                headers={"Authorization": f"Bearer {token}"},
                timeout=5
            )
            if me_response.status_code == 200:
                user_data = me_response.json()
                print(f"         Role: {user_data.get('role')} | DoctorID: {user_data.get('doctor_id')}")
            else:
                print(f"         [WARNING] Could not fetch profile data for {username}")
        else:
            print(f"[FAILED] {username} login failed. Status code: {response.status_code}")
            print(f"         Error: {response.text}")
    except requests.exceptions.ConnectionError:
        print(f"[ERROR] Could not connect to server at {base_url}. Make sure the server is running.")
        break
    except Exception as e:
        print(f"[ERROR] An error occurred for {username}: {str(e)}")

print("-" * 30)
print("Verification Complete.")
