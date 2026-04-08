import sys
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.test import Client

c = Client()
response = c.post('/admin/login/', {'username': 'boss', 'password': 'boss123', 'next': '/admin/'}, follow=True)
print("Login status code:", response.status_code)

if response.status_code == 200:
    if "Please enter the correct username and password" in response.content.decode('utf-8'):
        print("FAILED: Admin login rejected the credentials.")
    else:
        print("SUCCESS: Logged in properly (no error message found).")
else:
    print("Unexpected status code:", response.status_code)
