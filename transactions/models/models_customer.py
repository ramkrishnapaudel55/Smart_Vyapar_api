# from django.db import models
# from django.conf import settings
# from generic.models import GenericIdEntity

# User = settings.AUTH_USER_MODEL

# class Customer(GenericIdEntity):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     phone = models.CharField(max_length=15, blank=True)
#     address = models.CharField(max_length=255, blank=True)

#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name

#     class Meta:
#         db_table = 'customer'
#         managed = True