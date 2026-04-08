from api.models import User
import sys

try:
    # 1. Handle Haripriya
    u = User.objects.filter(doctor_id='20261102').first() or User.objects.filter(username='Haripriya').first()
    if not u:
        u = User.objects.create_user(username='Haripriya', password='Saveetha_Dental')
        print("Created new user Haripriya")
    else:
        print(f"Updating existing user: {u.username}")

    u.username = 'Haripriya'
    u.doctor_id = '20261102'
    u.role = 'CONSULTANT'
    u.specialization = 'Oral Medicine'
    u.first_name = 'Haripriya'
    u.set_password('Saveetha_Dental')
    u.save()

    # 2. Update all passwords to Saveetha_Dental (just in case new users were added without it)
    count = 0
    for user in User.objects.all():
        user.set_password('Saveetha_Dental')
        user.save()
        count += 1
    
    print(f"Successfully updated/verified {count} users with default password.")

except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
