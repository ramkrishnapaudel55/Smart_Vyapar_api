from django.db import models
from django.conf import settings
from generic.models import GenericIdEntity
from .models_transaction import Customer
from .models_product import Product

User = settings.AUTH_USER_MODEL

class Sales(GenericIdEntity):
    PAYMENT_MODES = (
        ('CASH', 'Cash'),
        ('CARD', 'Card'),
        ('ONLINE', 'Online'),
        ('CREDIT', 'Credit'),
    )
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('PROCESSING', 'Processing'),
        ('CANCELLED', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sales')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    total = models.DecimalField(max_digits=12, decimal_places=2)
    payment_mode = models.CharField(max_length=10, choices=PAYMENT_MODES, default='CASH')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='COMPLETED')
    date = models.DateField()
    image = models.ImageField(upload_to='sales_invoices/', null=True, blank=True)

    def __str__(self):
        return f"Sale #{self.id} - {self.product} - {self.total}"

    class Meta:
        db_table = 'sales'
        managed = True
