from django.urls import path
from .views import RegisterAPIView, VerifyEmailAPIView

urlpatterns = [
    path('api/register/', RegisterAPIView.as_view(), name='register'),
    path('api/verify-email/<str:token>/', VerifyEmailAPIView.as_view(), name='verify-email'),
]
