from django.urls import path
from .views import (
    UserViewSet, PatientViewSet, XRayScanViewSet, 
    AuditLogViewSet, AdminStatsViewSet, RolePermissionViewSet,
    DoctorDashboardStatsViewSet, LogEntryViewSet, AICertificationViewSet,
    SecuritySettingViewSet, SuggestionsViewSet, TreatmentPlanViewSet
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import ForgotPasswordView, VerifyOTPView, ResetPasswordView, LogoutView

urlpatterns = [
    # Auth Endpoints
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('auth/verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('auth/reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),

    # Users
    path('users/', UserViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('users/me/', UserViewSet.as_view({'get': 'me'})),
    path('users/profile/', UserViewSet.as_view({'get': 'profile', 'put': 'profile', 'patch': 'profile'})),
    path('users/upload_profile_picture/', UserViewSet.as_view({'post': 'upload_profile_picture'})),
    path('users/<str:pk>/', UserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),

    # Patients
    path('patients/', PatientViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('patients/booked_slots/', PatientViewSet.as_view({'get': 'booked_slots'})),
    path('patients/set_schedule/', PatientViewSet.as_view({'post': 'set_schedule'})),
    path('patients/today_schedule/', PatientViewSet.as_view({'get': 'today_schedule'})),
    path('patients/delete_by_id/', PatientViewSet.as_view({'delete': 'delete_by_id'})),
    path('patients/update_treatment/', PatientViewSet.as_view({'post': 'update_treatment'})),
    path('patients/recommend_drugs/', PatientViewSet.as_view({'post': 'recommend_drugs'})),
    path('patients/<str:pk>/upload-xray/', PatientViewSet.as_view({'post': 'upload_xray'})),
    path('patients/<str:pk>/', PatientViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),

    # X-Rays
    path('xrays/', XRayScanViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('xrays/diagnose/', XRayScanViewSet.as_view({'get': 'diagnose'})),
    path('xrays/upload/', XRayScanViewSet.as_view({'post': 'upload'})),
    path('xrays/<str:pk>/', XRayScanViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),

    # Logs
    path('logs/', AuditLogViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('logs/<str:pk>/', AuditLogViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('log-entries/', LogEntryViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('log-entries/<str:pk>/', LogEntryViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),

    # General / Stats Endpoints
    path('admin-stats/', AdminStatsViewSet.as_view({'get': 'list'})),
    path('doctor-dashboard-stats/', DoctorDashboardStatsViewSet.as_view({'get': 'list'})),
    path('ai-certification/', AICertificationViewSet.as_view({'get': 'list'})),
    path('suggestions/', SuggestionsViewSet.as_view({'get': 'list'})),
    path('treatment-plans/', TreatmentPlanViewSet.as_view({'get': 'list'})),

    # Roles and Settings (Custom Lookups)
    path('role-permissions/', RolePermissionViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('role-permissions/<str:role>/', RolePermissionViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    
    path('security-settings/', SecuritySettingViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('security-settings/<str:setting_id>/', SecuritySettingViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
]
