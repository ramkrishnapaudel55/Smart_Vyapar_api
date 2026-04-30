from django.db import models
from django.conf import settings
from generic.models import GenericIdEntity
from .models_product_category import ProductCategory

User = settings.AUTH_USER_MODEL

class Product(GenericIdEntity):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=100, blank=True)
    quantity = models.IntegerField(default=0)
    cost_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    selling_price = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')

    def __str__(self):
        return f"{self.name} ({self.model})" if self.model else self.name

    class Meta:
        db_table = 'products'
        managed = True
