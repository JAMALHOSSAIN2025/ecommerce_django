from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        email = "jabaka11@yahoo.com"
        password = "SuperStrongPassword123"  # নতুন পাসওয়ার্ড
        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(
                email=email,
                username="adminrender",
                password=password
            )
            self.stdout.write(self.style.SUCCESS("✅ Superuser created on Render"))
        else:
            self.stdout.write("⚠️ Superuser already exists.")
