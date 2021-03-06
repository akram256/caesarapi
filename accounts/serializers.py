import re
from django.contrib.auth import authenticate
from random import randint
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from accounts.models import User



class RegistrationSerializer(serializers.ModelSerializer):
    """Serializer registration requests and create a new user."""

    password = serializers.CharField(
        max_length=128,
        min_length=6,
        write_only=True,
        error_messages={
            "min_length": "Password should be at least {min_length} characters"
        }
    )
    confirmed_password = serializers.CharField(
        max_length=128,
        min_length=6,
        write_only=True,
        error_messages={
            "min_length": "Password should be at least {min_length} characters"
        }
    )

    class Meta:
        model = User
        fields = ["email", "phone_no", "first_name", "last_name",
                  "password", "confirmed_password",
                #    "username",
                   ]

    def validate(self, data):
        """Validate data before it gets saved."""

        confirmed_password = data.get("confirmed_password")
        try:
            validate_password(data["password"])
        except ValidationError as identifier:
            raise serializers.ValidationError({
                "password": str(identifier).replace(
                    "["", "").replace(""]", "")})

        if not self.do_passwords_match(data["password"], confirmed_password):
            raise serializers.ValidationError({
                "passwords": ("Passwords do not match")
            })

        return data

    def create(self, validated_data):
        """Create a user."""
        del validated_data["confirmed_password"]
        return User.objects.create_user(**validated_data)

    def do_passwords_match(self, password1, password2):
        """Check if passwords match."""
        return password1 == password2



class LoginSerializer(serializers.Serializer):
    # email = serializers.CharField(write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    # Ignore these fields if they are included in the request.
    username = serializers.CharField(max_length=255, read_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate_phone_no(self, value):
        if not value:
            raise serializers.ValidationError(
                'An phone_no is required to log in.'
            )
        return value 
    def validate_password(self, value):
        if value is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )
        return value