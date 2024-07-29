from authentication.models import User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68,
        min_length=6,
        write_only=True,
        style={"input_type": "password"})

    class Meta:
        model = User
        fields = ["email", "password"]

    # Deactivate account until it is verified
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.is_active = False
        user.save()
        return user

    def validate_email(self, email):
        lower_email = email.lower()
        if User.objects.filter(email__iexact=lower_email).exists():
            raise serializers.ValidationError("Duplicate email")
        return lower_email

    def get_verification_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
