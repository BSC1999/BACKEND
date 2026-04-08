from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Patient, XRayScan, AuditLog, RolePermission, SecuritySetting

# mawa, using CustomUserAdmin to handle password hashing and custom fields properly
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ["username", "email", "doctor_id", "role", "is_staff"]
    
    # Adding our custom fields to the admin forms
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("doctor_id", "phone", "specialization", "role", "status", "profile_picture", "reminders_enabled")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Info", {"fields": ("doctor_id", "phone", "specialization", "role", "status", "profile_picture", "reminders_enabled")}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Patient)
admin.site.register(XRayScan)
admin.site.register(AuditLog)
admin.site.register(RolePermission)
admin.site.register(SecuritySetting)
