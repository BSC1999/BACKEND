from api.models import User
users = User.objects.filter(role='CONSULTANT')
if not users.exists():
    print("NO_CONSULTANT_FOUND")
else:
    for u in users:
        print(f"User: {u.username}")
        print(f"Active: {u.is_active}")
        print(f"Staff: {u.is_staff}")
        print(f"PasswordHashed: {u.password.startswith('pbkdf2')}")
        print(f"IsAuthenticatedCheck: {u.check_password('test1234')}") # checking with a common test password if user mentions it
        print("-" * 10)
