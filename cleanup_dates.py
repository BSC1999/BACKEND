import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.models import Patient

qs = Patient.objects.exclude(next_schedule_date=None)
count = 0
for p in qs:
    if p.next_schedule_date and ("'" in p.next_schedule_date or '"' in p.next_schedule_date):
        original = p.next_schedule_date
        p.next_schedule_date = original.strip("'").strip('"')
        p.save()
        count += 1
        print(f"Cleaned {p.name}: {original} -> {p.next_schedule_date}")

print(f"Total cleaned: {count}")
