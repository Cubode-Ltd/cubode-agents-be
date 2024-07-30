from django.urls import path
from .views import (
    RegisterAPIView,
    LoginAPIView,
    VerifyEmailAPIView,
    PasswordResetAPIView,
    PasswordResetConfirmAPIView
)

urlpatterns = [
    path('api/register/', RegisterAPIView.as_view(), name='register'),
    path('api/login/', LoginAPIView.as_view(), name='register'),
    path('api/verify-email/<str:token>/', VerifyEmailAPIView.as_view(), name='verify-email'),
    path('api/password-reset/', PasswordResetAPIView.as_view(), name='password-reset'),
    path('api/password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmAPIView.as_view(), name='password-reset-confirm'),
]
