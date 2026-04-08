import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.models import User

users_data = [
    {"username": "Ashwin", "role": "INTERN", "doctor_id": "20262201", "password": "Saveetha_Dental"},
    {"username": "Bharath", "role": "INTERN", "doctor_id": "20262202", "password": "Saveetha_Dental"},
    {"username": "Noor Fathima", "role": "INTERN", "doctor_id": "20262203", "password": "Saveetha_Dental"},
    {"username": "Vishal", "role": "INTERN", "doctor_id": "20262204", "password": "Saveetha_Dental"},
    {"username": "Prithiksha", "role": "INTERN", "doctor_id": "20262205", "password": "Saveetha_Dental"},
    {"username": "Sukanth", "role": "INTERN", "doctor_id": "20262206", "password": "Saveetha_Dental"},
    {"username": "Pratheeksha", "role": "INTERN", "doctor_id": "20262207", "password": "Saveetha_Dental"},
    {"username": "Srinivasan", "role": "INTERN", "doctor_id": "20262208", "password": "Saveetha_Dental"},
    {"username": "Sudev", "role": "INTERN", "doctor_id": "20262209", "password": "Saveetha_Dental"},
    {"username": "Sadhana", "role": "INTERN", "doctor_id": "20262210", "password": "Saveetha_Dental"},
    {"username": "Pradeepa", "role": "ASSISTANT", "doctor_id": "20263301", "password": "Saveetha_Dental"},
    {"username": "Vanitha", "role": "ASSISTANT", "doctor_id": "20263302", "password": "Saveetha_Dental"},
    {"username": "Tamil", "role": "ASSISTANT", "doctor_id": "20263303", "password": "Saveetha_Dental"},
    {"username": "Reshma", "role": "ASSISTANT", "doctor_id": "20263304", "password": "Saveetha_Dental"},
    {"username": "Aishwarya", "role": "ASSISTANT", "doctor_id": "20263305", "password": "Saveetha_Dental"},
]

def add_users():
    for data in users_data:
        try:
            # Check if user already exists
            user, created = User.objects.get_or_create(
                username=data["username"],
                defaults={
                    "role": data["role"],
                    "doctor_id": data["doctor_id"],
                    "first_name": data["username"].split()[0],
                    "last_name": " ".join(data["username"].split()[1:]) if " " in data["username"] else ""
                }
            )
            if created:
                user.set_password(data["password"])
                user.save()
                print(f"User {data['username']} created successfully.")
            else:
                user.role = data["role"]
                user.doctor_id = data["doctor_id"]
                user.set_password(data["password"])
                user.save()
                print(f"User {data['username']} updated successfully.")
        except Exception as e:
            print(f"Error adding user {data['username']}: {e}")

if __name__ == "__main__":
    add_users()
