# flake8: noqa: E501
from django.urls import path, re_path

from authentication.views import (
    Registration,
    Login,
    RecoverPassword,
    IsAuthenticatedView,
    RegisterAPIView,
    LoginAPIView,
    LogoutAPIView,
    VerifyEmailAPIView,
    PasswordResetAPIView,
    PasswordResetConfirmAPIView,
)

urlpatterns = [
    # Static Views
    re_path(r"^register/?$", Registration.as_view(), name="registration"),
    re_path(r"^login/?$", Login.as_view(), name="login"),
    re_path(
        r"^recover_password/?$", RecoverPassword.as_view(), name="recover-password"
    ),
    # API Views
    path("api/register/", RegisterAPIView.as_view(), name="register-api"),
    path("api/login/", LoginAPIView.as_view(), name="login-api"),
    path("api/logout/", LogoutAPIView.as_view(), name="logout-api"),
    path(
        "api/verify-email/<str:token>/",
        VerifyEmailAPIView.as_view(),
        name="verify-email",
    ),
    path("api/password-reset/", PasswordResetAPIView.as_view(), name="password-reset"),
    path(
        "api/password-reset-confirm/<uidb64>/<token>/",
        PasswordResetConfirmAPIView.as_view(),
        name="password-reset-confirm",
    ),
    re_path(
        r"^api/is-authenticated/?$",
        IsAuthenticatedView.as_view(),
        name="is_authenticated_api",
    ),
]
