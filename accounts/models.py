# accounts/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    is_google_user = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    username = models.CharField(max_length=150, blank=True, null=True)  # optional
    USERNAME_FIELD = 'email'           # ✅ email দিয়ে login হবে
    REQUIRED_FIELDS = ['username']     # ✅ createsuperuser এর জন্য

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.full_name or self.user.email
