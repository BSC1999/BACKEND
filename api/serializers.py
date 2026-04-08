from rest_framework import serializers  # type: ignore
from .models import (  # type: ignore
    User,
    Patient,
    XRayScan,
    AuditLog,
    RolePermission,
    SecuritySetting,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:  # type: ignore
        model = User
        fields = [
            "id",
            "doctor_id",
            "username",
            "email",
            "first_name",
            "last_name",
            "phone",
            "specialization",
            "role",
            "status",
            "profile_picture",
            "reminders_enabled",
        ]


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:  # type: ignore
        model = User
        fields = [
            "doctor_id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "phone",
            "specialization",
            "role",
            "status",
            "profile_picture",
            "reminders_enabled",
        ]

    def validate_email(self, value):
        if not value.lower().endswith('@gmail.com'):
            raise serializers.ValidationError("Only @gmail.com email addresses are allowed.")
        return value.lower()

    def validate_doctor_id(self, value):
        if len(str(value)) != 10:
            raise serializers.ValidationError("Doctor ID must be exactly 10 digits.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class RolePermissionSerializer(serializers.ModelSerializer):
    class Meta:  # type: ignore
        model = RolePermission
        fields = "__all__"


class XRayScanSerializer(serializers.ModelSerializer):
    class Meta:  # type: ignore
        model = XRayScan
        fields = "__all__"


class PatientSerializer(serializers.ModelSerializer):
    xrays = XRayScanSerializer(many=True, read_only=True)

    class Meta:  # type: ignore
        model = Patient
        fields = [
            "id",
            "patient_id",
            "name",
            "age",
            "dob",
            "gender",
            "phone",
            "email",
            "address",
            "complaint",
            "medical_history",
            "treatment_payment_info",
            "is_female",
            "added_timestamp",
            "assigned_doctor",
            "assigned_doctor_name",
            "next_schedule_date",
            "next_schedule_time",
            "last_visit_date",
            "xrays",
        ]
        read_only_fields = [
            "id",
            "added_timestamp",
            "assigned_doctor",
            "assigned_doctor_name",
        ]
        extra_kwargs = {
            "patient_id": {"required": True},
            "dob": {"required": False, "allow_null": True, "allow_blank": True},
            "address": {"required": False, "allow_null": True, "allow_blank": True},
            "email": {"required": False, "allow_null": True, "allow_blank": True},
            "complaint": {"required": False, "allow_null": True, "allow_blank": True},
            "medical_history": {"required": False, "allow_null": True, "allow_blank": True},
            "treatment_payment_info": {"required": False, "allow_null": True, "allow_blank": True},
            "next_schedule_date": {"required": False, "allow_null": True, "allow_blank": True},
            "next_schedule_time": {"required": False, "allow_null": True, "allow_blank": True},
            "last_visit_date": {"required": False, "allow_null": True, "allow_blank": True},
        }

    def validate_email(self, value):
        if value and not value.lower().endswith('@gmail.com'):
            raise serializers.ValidationError("Only @gmail.com email addresses are allowed.")
        return value.lower() if value else value


class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:  # type: ignore
        model = AuditLog
        fields = "__all__"


# Explicit alias for LogEntry.java integration


class LogEntrySerializer(serializers.ModelSerializer):
    userName = serializers.CharField(source="user_name", read_only=True)
    timestamp = serializers.DateTimeField(
        source="created_at", format="%d/%m/%Y %H:%M:%S", read_only=True
    )
    timeMillis = serializers.SerializerMethodField()
    ipAddress = serializers.CharField(source="ip_address", read_only=True)

    class Meta:  # type: ignore
        model = AuditLog
        fields = [
            "id",
            "userName",
            "role",
            "activity",
            "timestamp",
            "ipAddress",
            "timeMillis",
        ]

    def get_timeMillis(self, obj):
        return int(obj.created_at.timestamp() * 1000)


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not value.lower().endswith('@gmail.com'):
            raise serializers.ValidationError("Only @gmail.com email addresses are allowed.")
        return value.lower()


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate_email(self, value):
        if not value.lower().endswith('@gmail.com'):
            raise serializers.ValidationError("Only @gmail.com email addresses are allowed.")
        return value.lower()


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        if not value.lower().endswith('@gmail.com'):
            raise serializers.ValidationError("Only @gmail.com email addresses are allowed.")
        return value.lower()


class SecuritySettingSerializer(serializers.ModelSerializer):
    class Meta:  # type: ignore
        model = SecuritySetting
        fields = "__all__"
