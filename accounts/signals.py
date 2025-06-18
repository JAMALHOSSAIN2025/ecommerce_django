# accounts/signals.py

# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import CustomUser

# Auto-create profile when user is created
# @receiver(post_save, sender=CustomUser)
# def create_or_update_user_profile(sender, instance, created, **kwargs):
#    if created:
#       Profile.objects.create(user=instance)
#   else:
#        instance.profile.save()


# Middleware: Redirect if phone number not set (e.g., via Google login)
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect

class GoogleLoginRedirectMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            if not request.user.phone_number and request.path != '/complete-profile/':
                return redirect('complete_profile')
        return None
