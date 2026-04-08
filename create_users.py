from api.models import User
from django.contrib.auth.hashers import make_password

# List of users to create
users_to_create = [
    {"username": "admin_777", "doctor_id": "ADMIN_777", "role": "ADMIN", "first_name": "System", "last_name": "Admin"},
    {"username": "doctor_111", "doctor_id": "111001", "role": "DOCTOR", "first_name": "Senior", "last_name": "Doctor"},
    {"username": "consultant_222", "doctor_id": "222001", "role": "CONSULTANT", "first_name": "Expert", "last_name": "Consultant"},
    {"username": "assistant_333", "doctor_id": "333001", "role": "ASSISTANT", "first_name": "Medical", "last_name": "Assistant"},
]

password = "Saveetha_Dental"

for user_data in users_to_create:
    user, created = User.objects.get_or_create(
        username=user_data["username"],
        defaults={
            "doctor_id": user_data["doctor_id"],
            "role": user_data["role"],
            "first_name": user_data["first_name"],
            "last_name": user_data["last_name"],
            "email": f"{user_data['username']}@example.com",
            "password": make_password(password)
        }
    )
    if created:
        print(f"Created user: {user.username} with role {user.role}")
    else:
        # Update existing user to ensure correct role and password for testing
        user.doctor_id = user_data["doctor_id"]
        user.role = user_data["role"]
        user.password = make_password(password)
        user.save()
        print(f"Updated user: {user.username} with role {user.role}")

print("User creation/update complete.")
