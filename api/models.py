from django.db import models  # type: ignore
from django.contrib.auth.models import AbstractUser  # type: ignore
import uuid  # type: ignore
from django.utils import timezone  # type: ignore
from datetime import timedelta  # type: ignore


class User(AbstractUser):
    # Overriding standard user model to add Doctor/Admin specific fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctor_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    specialization = models.CharField(max_length=100, null=True, blank=True)

    ROLE_CHOICES = (
        ("ADMIN", "Admin"),
        ("DOCTOR", "Doctor"),
        ("CONSULTANT", "Consultant"),
        ("ASSISTANT", "Assistant"),
        ("INTERN", "Intern"),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="DOCTOR")

    STATUS_CHOICES = (
        ("ACTIVE", "Active"),
        ("INACTIVE", "Inactive"),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ACTIVE")
    profile_picture = models.ImageField(upload_to="profiles/", null=True, blank=True)
    reminders_enabled = models.BooleanField(default=False)  # type: ignore

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.role}"


class RolePermission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=50, unique=True, choices=User.ROLE_CHOICES)
    can_add_patient = models.BooleanField(default=True)  # type: ignore
    can_edit_patient = models.BooleanField(default=True)  # type: ignore
    can_delete_patient = models.BooleanField(default=False)  # type: ignore
    can_add_doctor = models.BooleanField(default=False)  # type: ignore
    can_view_analytics = models.BooleanField(default=True)  # type: ignore
    can_view_audit_logs = models.BooleanField(default=False)  # type: ignore
    can_manage_settings = models.BooleanField(default=False)  # type: ignore
    can_use_ai = models.BooleanField(default=True)  # type: ignore
    can_prescribe_drugs = models.BooleanField(default=True)  # type: ignore
    can_view_patients = models.BooleanField(default=True)  # type: ignore

    def __str__(self):
        return f"Permissions for {self.role}"


class Patient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    age = models.IntegerField()
    dob = models.CharField(max_length=50, blank=True, null=True, default="N/A")
    gender = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    email = models.EmailField(null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    complaint = models.TextField(blank=True, null=True)
    medical_history = models.TextField(blank=True, null=True)
    allergies = models.TextField(blank=True, null=True, default="None")
    treatment_payment_info = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        default="No treatment/payment info recorded",
    )
    is_female = models.BooleanField(default=False)  # type: ignore
    added_timestamp = models.DateTimeField(auto_now_add=True)
    assigned_doctor = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="patients"
    )
    assigned_doctor_name = models.CharField(
        max_length=100, default="General", blank=True
    )
    next_schedule_date = models.CharField(max_length=50, blank=True, null=True)
    next_schedule_time = models.CharField(max_length=50, blank=True, null=True)
    last_visit_date = models.CharField(max_length=50, blank=True, null=True, default="N/A")

    def __str__(self):
        return f"{self.name} ({self.patient_id})"


class XRayScan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="xrays")
    image = models.ImageField(upload_to="xrays/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"XRay for {self.patient.name} on {self.uploaded_at}"


class AuditLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_name = models.CharField(max_length=100)
    role = models.CharField(max_length=50)
    activity = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.created_at}] {self.user_name}: {self.activity}"


class OTPRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="otp_requests"
    )
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)  # type: ignore

    def is_valid(self):
        # OTP valid for 10 minutes
        if self.is_used:
            return False
        return timezone.now() <= self.created_at + timedelta(minutes=10)

    def __str__(self):
        email = getattr(self.user, "email", "")
        return f"OTP for {email} - {'Used' if self.is_used else 'Available'}"


class SecuritySetting(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    setting_id = models.CharField(max_length=50, unique=True, default="GLOBAL")
    two_factor_enabled = models.BooleanField(default=False)  # type: ignore
    aggressive_path_detection = models.BooleanField(default=True)  # type: ignore
    vital_overlay = models.BooleanField(default=False)  # type: ignore
    ultra_dark_mode = models.BooleanField(default=True)  # type: ignore
    dicom_mirror = models.BooleanField(default=True)  # type: ignore
    password_policy_strictness = models.CharField(max_length=50, default="Medium")

    def __str__(self):
        return f"Settings for {self.setting_id}"
