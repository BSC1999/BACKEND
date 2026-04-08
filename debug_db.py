import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.models import Patient

now = timezone.localtime(timezone.now())
today_iso = now.strftime("%Y-%m-%d")
today_indian = now.strftime("%d-%m-%Y")

print(f"DEBUG: Server Time (localtime): {now}")
print(f"DEBUG: Search Pattern ISO: {today_iso}")
print(f"DEBUG: Search Pattern Indian: {today_indian}")

patients = Patient.objects.all()
print(f"DEBUG: Total Patients in DB: {patients.count()}")

for p in patients:
    print(f"ID: {p.id} Name: {p.name} Scheduled: |{p.next_schedule_date}| Doctor: |{p.assigned_doctor_name}|")
    if today_iso in str(p.next_schedule_date) or today_indian in str(p.next_schedule_date):
        print(f"  >>> MATCHES TODAY!")
