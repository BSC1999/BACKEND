import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.models import User

def remove_consultants():
    try:
        # Since we removed it from choices, it might still exist in the DB as a string
        consultants = User.objects.filter(role="CONSULTANT")
        count = consultants.count()
        consultants.delete()
        print(f"Successfully deleted {count} Consultant users.")
    except Exception as e:
        print(f"Error removing consultant users: {e}")

if __name__ == "__main__":
    remove_consultants()
