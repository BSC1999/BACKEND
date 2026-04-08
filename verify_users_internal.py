from api.models import User
from django.contrib.auth import authenticate

users = [
    "admin_777",
    "doctor_111",
    "consultant_222",
    "assistant_333",
    "testdoctor"
]

password = "Saveetha_Dental"

print("Starting Internal Login Verification...")
print("-" * 30)

for username in users:
    user = authenticate(username=username, password=password)
    if user:
        print(f"[SUCCESS] {username} authenticated successfully.")
        print(f"         Role: {user.role} | DoctorID: {user.doctor_id}")
    else:
        print(f"[FAILED] {username} authentication failed.")
        # Check if user exists but password mismatch
        if User.objects.filter(username=username).exists():
            print(f"         [DEBUG] User exists but password/auth failed.")
        else:
            print(f"         [DEBUG] User '{username}' does not exist in DB.")

print("-" * 30)
print("Internal Verification Complete.")
