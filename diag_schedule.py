import os
import django
from datetime import datetime
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.models import Patient
from django.db import models

today_iso = datetime.now().strftime("%Y-%m-%d")
today_indian = datetime.now().strftime("%d-%m-%Y")

print(f"Searching for: {today_iso} or {today_indian}")

# Try direct filter
patients = Patient.objects.filter(
    models.Q(next_schedule_date=today_iso) | 
    models.Q(next_schedule_date=today_indian)
)

print(f"Direct match count: {patients.count()}")

# Try contains
patients_contains = Patient.objects.filter(
    models.Q(next_schedule_date__contains=today_iso) | 
    models.Q(next_schedule_date__contains=today_indian)
)
print(f"Contains count: {patients_contains.count()}")

# Show all non-null dates
all_dates = list(Patient.objects.exclude(next_schedule_date=None).values_list('name', 'next_schedule_date', 'assigned_doctor_name'))
print("All Scheduled Patients:")
for name, date, doc in all_dates:
    print(f" - {name}: |{date}| (Doc: {doc})")
