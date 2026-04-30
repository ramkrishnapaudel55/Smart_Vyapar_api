from django.db import models
from django.conf import settings
from generic.models import GenericIdEntity

User = settings.AUTH_USER_MODEL

class ProductCategory(GenericIdEntity):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_categories')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'product_categories'
        managed = True
        unique_together = ('user', 'name')

    def __str__(self):
        return self.name
