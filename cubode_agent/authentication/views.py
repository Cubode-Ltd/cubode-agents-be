from authentication.serializer import RegisterSerializer
from authentication.utils import send_template_email

from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


User = get_user_model()


class VerifyEmailAPIView(APIView):
    def get(self, request, token):
        try:
            UntypedToken(token)
            user_id = UntypedToken(token)['user_id']
            user = User.objects.get(id=user_id)
            if not user.is_active:
                user.is_active = True
                user.save()
            return Response({
                'message': 'Email successfully verified.'
                }, status=status.HTTP_200_OK)

        except (InvalidToken, TokenError):
            return Response({
                'error': 'Invalid token'
                }, status=status.HTTP_400_BAD_REQUEST)


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = serializer.get_verification_token(user)
            verification_url = request.build_absolute_uri(
                reverse('verify-email', kwargs={'token': token})
            )

            send_template_email(
                template="templates/registration_email.html",
                to=user.email,
                subj="Cubode - Verify your Email",
                template_name=user.username,
                template_url_verification=verification_url,
                sender=settings.EMAIL_SENDER,
                fail_silently=False,
            )

            return Response({
                'message': "Registration successful. Please check your email for verification."},
                status=status.HTTP_201_CREATED)

        print(serializer.errors)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST)
