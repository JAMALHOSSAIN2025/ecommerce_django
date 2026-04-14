from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # 🟢 STOCK SYSTEM (NEW)
    stock = models.PositiveIntegerField(default=0)

    # 🖼 IMAGE FIELD (optional but common in ecommerce)
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    # 🕒 TIMESTAMP
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    # 🧠 Helper: is product available?
    def is_in_stock(self):
        return self.stock > 0

    # 🧠 Helper: safe stock check
    def can_purchase(self, quantity):
        return self.stock >= quantity