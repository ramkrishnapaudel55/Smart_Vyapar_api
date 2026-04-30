from generic.models import GenericIdEntity
from django.db import models

class Role(GenericIdEntity):
    ROLE_CHOICES = (
        ('PATIENT', 'Patient'),
        ('CAREGIVER', 'Caregiver'),
    )

    name = models.CharField(max_length=20, choices=ROLE_CHOICES, unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'role'
        managed = True