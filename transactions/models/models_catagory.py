from django.db import models
from django.conf import settings
from generic.models import GenericIdEntity

User = settings.AUTH_USER_MODEL


class Category(GenericIdEntity):
    CATEGORY_TYPE = (
        ('INCOME', 'income'),
        ('EXPENSE', 'expense'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)
    category_type = models.CharField(max_length=10, choices=CATEGORY_TYPE)
   
    class Meta:
        db_table = 'categories'
        unique_together = ('user', 'name', 'category_type')
        managed = True

    def __str__(self):
        return self.name
