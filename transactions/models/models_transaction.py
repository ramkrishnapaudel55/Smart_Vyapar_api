from django.db import models
from django.conf import settings
from generic.models import GenericIdEntity
from transactions.models import Category

User = settings.AUTH_USER_MODEL

class Customer(GenericIdEntity):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=255, blank=True)
    test_field = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'customer'
        managed = True
        

class Transaction(GenericIdEntity):
    TRANSACTION_TYPE = (
        ('INCOME', 'income'),
        ('EXPENSE', 'expense'),
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE)
    description = models.TextField(blank=True)
    date = models.DateField()

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"
    
    class Meta:
        db_table = 'transactions'
        managed = True
