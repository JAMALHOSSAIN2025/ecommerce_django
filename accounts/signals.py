# accounts/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, Profile

@receiver(post_save, sender=CustomUser)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    যখনই নতুন CustomUser তৈরি হবে, তার জন্য একটি Profile তৈরি হবে।
    যদি Profile আগে থেকেই থাকে, তাহলে সেটি শুধু save হবে।
    """
    if created:
        # নতুন ইউজারের জন্য নতুন প্রোফাইল তৈরি করো
        Profile.objects.create(user=instance)
        print(f'✅ Profile created for user: {instance.email}')
    else:
        # শুধু নিশ্চিত হও profile থেকে profile.save() হচ্ছে
        if hasattr(instance, 'profile'):
            instance.profile.save()
        else:
            # fallback যদি profile না থাকে
            Profile.objects.create(user=instance)
            print(f'⚠️ Profile missing — created fallback for user: {instance.email}')
