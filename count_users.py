from api.models import User
from django.db.models import Count
import json

total = User.objects.count()
roles = User.objects.values('role').annotate(count=Count('role'))

result = {
    "total": total,
    "breakdown": {r['role']: r['count'] for r in roles}
}
print(json.dumps(result))
