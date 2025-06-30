# accounts/serializers.py

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

User = get_user_model()


# ------------------ User Serializer ------------------

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username']  # You can add other fields if needed


# ------------------ JWT Login Serializer ------------------

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'  # Use email as username for login

    def validate(self, attrs):
        credentials = {
            'username': attrs.get('email'),  # Because default backend uses `username`
            'password': attrs.get('password')
        }

        user = authenticate(**credentials)
        if user is None:
            raise serializers.ValidationError('No active account found with the given credentials')

        data = super().validate(attrs)

        # Include user info in the response
        data['user'] = {
            'id': user.id,
            'email': user.email,
            'username': user.username,
        }

        return data


# ------------------ Register Serializer ------------------

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match")

        try:
            validate_password(data['password'])
        except ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})

        return data

    def create(self, validated_data):
        validated_data.pop('password2')  # Remove confirm password
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
