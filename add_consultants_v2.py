import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.models import User

consultants_data = [
    {"username": "Surenthar", "role": "CONSULTANT", "specialization": "Oral Medicine", "doctor_id": "20261101", "password": "Saveetha_Dental"},
    {"username": "Haripriya", "role": "CONSULTANT", "specialization": "Oral Medicine", "doctor_id": "20261102", "password": "Saveetha_Dental"},
    {"username": "Sangavi", "role": "CONSULTANT", "specialization": "Oral Medicine", "doctor_id": "20261103", "password": "Saveetha_Dental"},
    {"username": "Kirtana", "role": "CONSULTANT", "specialization": "Conservative Dentistry and Endodontics", "doctor_id": "20261104", "password": "Saveetha_Dental"},
    {"username": "Jitesh", "role": "CONSULTANT", "specialization": "Conservative Dentistry and Endodontics", "doctor_id": "20261105", "password": "Saveetha_Dental"},
    {"username": "Manobarathi", "role": "CONSULTANT", "specialization": "Conservative Dentistry and Endodontics", "doctor_id": "20261106", "password": "Saveetha_Dental"},
    {"username": "Harini Krish", "role": "CONSULTANT", "specialization": "Prosthodontics", "doctor_id": "20261107", "password": "Saveetha_Dental"},
    {"username": "Amrutha Shenoy", "role": "CONSULTANT", "specialization": "Prosthodontics", "doctor_id": "20261108", "password": "Saveetha_Dental"},
    {"username": "Kushali", "role": "CONSULTANT", "specialization": "Prosthodontics", "doctor_id": "20261109", "password": "Saveetha_Dental"},
    {"username": "Jayashree", "role": "CONSULTANT", "specialization": "Public Health Dentistry", "doctor_id": "20261110", "password": "Saveetha_Dental"},
    {"username": "Kavitha", "role": "CONSULTANT", "specialization": "Public Health Dentistry", "doctor_id": "20261111", "password": "Saveetha_Dental"},
    {"username": "Mohammed Muhsin", "role": "CONSULTANT", "specialization": "Public Health Dentistry", "doctor_id": "20261112", "password": "Saveetha_Dental"},
    {"username": "Karthikeyan Murthikumar", "role": "CONSULTANT", "specialization": "Periodontics", "doctor_id": "20261113", "password": "Saveetha_Dental"},
    {"username": "Parkavi", "role": "CONSULTANT", "specialization": "Periodontics", "doctor_id": "20261114", "password": "Saveetha_Dental"},
    {"username": "Arvina", "role": "CONSULTANT", "specialization": "Periodontics", "doctor_id": "20261115", "password": "Saveetha_Dental"},
    {"username": "Ekambareshwaran", "role": "CONSULTANT", "specialization": "Pedodontics", "doctor_id": "20261116", "password": "Saveetha_Dental"},
    {"username": "Maria ANthonet", "role": "CONSULTANT", "specialization": "Pedodontics", "doctor_id": "20261117", "password": "Saveetha_Dental"},
    {"username": "Dinesh", "role": "CONSULTANT", "specialization": "Pedodontics", "doctor_id": "20261118", "password": "Saveetha_Dental"},
    {"username": "Reshma", "role": "CONSULTANT", "specialization": "Oral Pathology", "doctor_id": "20261119", "password": "Saveetha_Dental"},
    {"username": "Abilasha", "role": "CONSULTANT", "specialization": "Oral Pathology", "doctor_id": "20261120", "password": "Saveetha_Dental"},
    {"username": "Deepak", "role": "CONSULTANT", "specialization": "Oral Pathology", "doctor_id": "20261121", "password": "Saveetha_Dental"},
]

def add_consultants():
    for data in consultants_data:
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
                print(f"Consultant {data['username']} created successfully.")
            else:
                user.role = data["role"]
                user.doctor_id = data["doctor_id"]
                user.specialization = data["specialization"]
                user.set_password(data["password"])
                user.save()
                print(f"Consultant {data['username']} updated successfully.")
        except Exception as e:
            print(f"Error adding consultant {data['username']}: {e}")

if __name__ == "__main__":
    add_consultants()
