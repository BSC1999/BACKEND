from api.models import User
import sys

user_data = [
    {"username": "Sangavi", "id": "20261103", "spec": "Oral Medicine"},
    {"username": "Kalyani", "id": "20261104", "spec": "Oral Surgery"},
    {"username": "Aiden", "id": "20261105", "spec": "Oral Surgery"},
    {"username": "Goutham", "id": "20261106", "spec": "Oral Surgery"},
    {"username": "Kirtana", "id": "20261107", "spec": "Conservative Dentistry and Endodontics"},
    {"username": "Jitesh", "id": "20261108", "spec": "Conservative Dentistry and Endodontics"},
    {"username": "Manobarathi", "id": "20261109", "spec": "Conservative Dentistry and Endodontics"},
    {"username": "Harini Krish", "id": "20261110", "spec": "Prosthodontics"},
    {"username": "Amrutha Shenoy", "id": "20261111", "spec": "Prosthodontics"},
    {"username": "Kushali", "id": "20261112", "spec": "Prosthodontics"},
    {"username": "Jayashree", "id": "20261113", "spec": "Public Health Dentistry"},
    {"username": "Kavitha", "id": "20261114", "spec": "Public Health Dentistry"},
    {"username": "Mohammed Muhsin", "id": "20261115", "spec": "Public Health Dentistry"},
    {"username": "Karthikeyan Murthikumar", "id": "20261116", "spec": "Periodontics"},
    {"username": "Parkavi", "id": "20261117", "spec": "Periodontics"},
    {"username": "Arvina", "id": "20261118", "spec": "Periodontics"},
    {"username": "Ekambareshwaran", "id": "20261119", "spec": "Pedodontics"},
    {"username": "Maria ANthonet", "id": "20261120", "spec": "Pedodontics"},
    {"username": "Dinesh", "id": "20261121", "spec": "Pedodontics"},
    {"username": "Prem Vishva", "id": "20261122", "spec": "Orthodontics"},
    {"username": "Dilip", "id": "20261123", "spec": "Orthodontics"},
    {"username": "Sruthi", "id": "20261124", "spec": "Orthodontics"},
    {"username": "Reshma", "id": "20261125", "spec": "Oral Pathology"},
    {"username": "Abilasha", "id": "20261126", "spec": "Oral Pathology"},
    {"username": "Deepak", "id": "20261127", "spec": "Oral Pathology"},
]

default_password = 'Saveetha_Dental'

try:
    print(f"Starting batch creation of {len(user_data)} users...")
    
    for data in user_data:
        # Normalize username to be lowercase-friendly or as provided? User provided with Caps.
        # Usernames in Django are usually case-sensitive but standard to match input.
        username = data["username"].replace(" ", "_").lower() # Using underscores for usernames to be safe
        
        u = User.objects.filter(doctor_id=data["id"]).first() or User.objects.filter(username=username).first()
        
        if not u:
            u = User.objects.create_user(username=username, password=default_password)
            print(f"Created user: {username}")
        else:
            print(f"Updating user: {u.username}")
            u.set_password(default_password)
        
        u.doctor_id = data["id"]
        u.role = 'CONSULTANT'
        u.specialization = data["spec"]
        u.first_name = data["username"]
        u.save()

    # Final pass to ensure EVERYONE has the same password as requested
    all_count = 0
    for user in User.objects.all():
        user.set_password(default_password)
        user.save()
        all_count += 1
    
    print(f"Finished. Total users in database: {all_count}")

except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
