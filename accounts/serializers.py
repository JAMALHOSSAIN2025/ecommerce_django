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
        fields = ['id', 'email', 'username']  # প্রয়োজন অনুযায়ী ফিল্ড বাড়াতে পারো


# ------------------ JWT Login Serializer ------------------

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'  # Login এর জন্য email ইউজ করবো

    def validate(self, attrs):
        # DRF authenticate expects 'username', তাই email দিয়ে username হিসেবে পাঠানো হচ্ছে
        credentials = {
            'username': attrs.get('email'),
            'password': attrs.get('password')
        }

        user = authenticate(**credentials)
        if user is None:
            raise serializers.ValidationError('No active account found with the given credentials')

        data = super().validate(attrs)

        # ইউজারের তথ্য রেসপন্সে যোগ করা হলো
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
            raise serializers.ValidationError({"password": "Passwords do not match"})

        try:
            validate_password(data['password'])
        except ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})

        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        username = validated_data.get('username', None)
        email = validated_data['email']
        password = validated_data['password']

        # username optional হলে এখানে লজিক দিতে পারো
        if username:
            user = User.objects.create_user(username=username, email=email, password=password)
        else:
            # username না থাকলে email দিয়েই ইউজার তৈরি করতে পারো (Depends on your User model)
            user = User.objects.create_user(email=email, password=password)

        return user
