from rest_framework import serializers
from .models import User, Patient, XRayScan, AuditLog, RolePermission, SecuritySetting

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'doctor_id', 'username', 'email', 'first_name', 'last_name', 'phone', 'specialization', 'role', 'status', 'profile_picture', 'reminders_enabled']

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['doctor_id', 'username', 'email', 'password', 'first_name', 'last_name', 'phone', 'specialization', 'role', 'status', 'profile_picture', 'reminders_enabled']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class RolePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolePermission
        fields = '__all__'

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

class XRayScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = XRayScan
        fields = '__all__'

class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = '__all__'

# Explicit alias for LogEntry.java integration
class LogEntrySerializer(serializers.ModelSerializer):
    userName = serializers.CharField(source='user_name', read_only=True)
    timestamp = serializers.DateTimeField(source='created_at', format='%d/%m/%Y %H:%M:%S', read_only=True)
    timeMillis = serializers.SerializerMethodField()
    ipAddress = serializers.CharField(source='ip_address', read_only=True)

    class Meta:
        model = AuditLog
        fields = ['id', 'userName', 'role', 'activity', 'timestamp', 'ipAddress', 'timeMillis']

    def get_timeMillis(self, obj):
        return int(obj.created_at.timestamp() * 1000)

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField(write_only=True)

class SecuritySettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecuritySetting
        fields = '__all__'
