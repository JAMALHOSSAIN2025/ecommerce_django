from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username']  # প্রয়োজন অনুযায়ী ফিল্ড অ্যাড/রিমুভ করো


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'  # বললাম ইউজারনেম হিসেবে email ব্যবহার করবো

    def validate(self, attrs):
        # এখানে attrs['email'], attrs['password'] থাকবে
        credentials = {
            'username': attrs.get('email'),  # ডিফল্ট authentication backend 'username' চায়
            'password': attrs.get('password')
        }

        user = authenticate(**credentials)
        if user is None:
            raise serializers.ValidationError('No active account found with the given credentials')

        # টোকেন জেনারেট করার জন্য parent class এর validate কল করবো
        data = super().validate(attrs)

        # যদি অতিরিক্ত ইউজার ডেটা দিতে চাও
        data['user'] = {
            'id': user.id,
            'email': user.email,
            'username': user.username
        }

        return data
