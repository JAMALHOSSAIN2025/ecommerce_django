from django.db import models
from django.utils import timezone
from django.conf import settings

class Product(models.Model):
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='products_as_seller',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='products_as_user',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True, default='default.jpg')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
