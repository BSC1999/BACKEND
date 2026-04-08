import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.models import User

doctors_data = [
    {"username": "Kalyani", "role": "DOCTOR", "specialization": "Oral Surgery", "doctor_id": "20260001", "password": "Saveetha_Dental"},
    {"username": "Aiden", "role": "DOCTOR", "specialization": "Oral Surgery", "doctor_id": "20260002", "password": "Saveetha_Dental"},
    {"username": "Goutham", "role": "DOCTOR", "specialization": "Oral Surgery", "doctor_id": "20260003", "password": "Saveetha_Dental"},
    {"username": "Prem Vishva", "role": "DOCTOR", "specialization": "Orthodontics", "doctor_id": "20260004", "password": "Saveetha_Dental"},
    {"username": "Dilip", "role": "DOCTOR", "specialization": "Orthodontics", "doctor_id": "20260005", "password": "Saveetha_Dental"},
    {"username": "Sruthi", "role": "DOCTOR", "specialization": "Orthodontics", "doctor_id": "20260006", "password": "Saveetha_Dental"},
]

def add_doctors():
    for data in doctors_data:
        try:
            user, created = User.objects.get_or_create(
                username=data["username"],
                defaults={
                    "role": data["role"],
                    "doctor_id": data["doctor_id"],
                    "specialization": data["specialization"],
                    "first_name": data["username"].split()[0],
                    "last_name": " ".join(data["username"].split()[1:]) if " " in data["username"] else ""
                }
            )
            if created:
                user.set_password(data["password"])
                user.save()
                print(f"Doctor {data['username']} created successfully.")
            else:
                user.role = data["role"]
                user.doctor_id = data["doctor_id"]
                user.specialization = data["specialization"]
                user.set_password(data["password"])
                user.save()
                print(f"Doctor {data['username']} updated successfully.")
        except Exception as e:
            print(f"Error adding doctor {data['username']}: {e}")

if __name__ == "__main__":
    add_doctors()
