from authentication.serializer import (
    RegisterSerializer,
    LoginSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
)
from authentication.utils import send_template_email

from django.contrib.auth import login, logout, get_user_model
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.shortcuts import render
from django.views import View

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

User = get_user_model()


# Static Views
class Registration(View):
    def get(self, request):
        return render(request, "register.html", {})


class Login(View):
    def get(self, request):
        return render(request, "login.html", {})


class RecoverPassword(View):
    def get(self, request):
        return render(request, "reset_password.html", {})


# API Views
class IsAuthenticatedView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_authenticated:
            user_data = {
                "username": request.user.username,
                "email": request.user.email,
                "is_authenticated": True,
            }
            return Response(user_data)
        else:
            return Response({"is_authenticated": False}, status=401)


class VerifyEmailAPIView(APIView):
    def get(self, request, token):
        try:
            UntypedToken(token)
            user_id = UntypedToken(token)["user_id"]
            user = User.objects.get(id=user_id)
            if not user.is_active:
                user.is_active = True
                user.save()
            return Response(
                {"message": "Email successfully verified."}, status=status.HTTP_200_OK
            )

        except (InvalidToken, TokenError):
            return Response(
                {"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = serializer.get_verification_token(user)
            verification_url = request.build_absolute_uri(
                reverse("verify-email", kwargs={"token": token})
            )

            context = {
                "username": user.email,
                "verification_url": verification_url,
            }

            send_template_email(
                template_name="registration_email.html",
                to=user.email,
                subject="Cubode - Verify your Email",
                context=context,
                sender=settings.EMAIL_SENDER,
            )

            return Response(
                {
                    "message": "Registration successful. Please check your email for verification."
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            login(request, user)

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            response = Response(
                {
                    "message": "Login successful",
                    "user": {
                        "email": user.email,
                        "username": user.username,
                    },
                },
                status=status.HTTP_200_OK,
            )

            response.set_cookie(
                key="refresh_token",
                value=str(refresh),
                httponly=True,
                secure=True,
                samesite="Lax",
                max_age=60 * 60 * 24 * 7,
            )

            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=True,
                samesite="Lax",
                max_age=60 * 60 * 24,
            )

            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            logout(request)
            refresh_token = request.COOKIES.get("refresh_token")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()

            # Clear the JWT tokens from cookies
            response = Response(
                {"message": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT
            )
            response.delete_cookie("refresh_token")
            response.delete_cookie("access_token")

            return response

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetAPIView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            reset_url = request.build_absolute_uri(
                reverse(
                    "password-reset-confirm", kwargs={"uidb64": uid, "token": token}
                )
            )

            context = {
                "username": user.email,
                "reset_url": reset_url,
            }

            send_template_email(
                template_name="reset_password_email.html",
                to=user.email,
                subject="Cubode - Reset your Password",
                context=context,
                sender=settings.EMAIL_SENDER,
            )

            return Response(
                {"message": "Password reset link has been sent to your email."},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmAPIView(APIView):
    def post(self, request, uidb64, token):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            try:
                uid = urlsafe_base64_decode(uidb64).decode()
                user = User.objects.get(pk=uid)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None

            if user is not None and default_token_generator.check_token(user, token):
                user.set_password(serializer.validated_data["new_password"])
                user.save()
                return Response(
                    {"message": "Password has been reset successfully."},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "Invalid token or user ID."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
