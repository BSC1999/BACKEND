from api.models import User
import sys

try:
    # 1. Handle Surenthar
    u = User.objects.filter(doctor_id='20261101').first() or User.objects.filter(username='surenthar').first()
    if not u:
        u = User.objects.create_user(username='surenthar', password='Saveetha_Dental')
        print("Created new user surenthar")
    else:
        print(f"Updating existing user: {u.username}")

    u.username = 'surenthar'
    u.doctor_id = '20261101'
    u.role = 'CONSULTANT'
    u.specialization = 'Oral Medicine'
    u.first_name = 'Surenthar'
    u.set_password('Saveetha_Dental')
    u.save()

    # 2. Update all passwords to Saveetha_Dental
    count = 0
    for user in User.objects.all():
        user.set_password('Saveetha_Dental')
        user.save()
        count += 1
    
    print(f"Successfully updated/verified {count} users with default password.")

except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
