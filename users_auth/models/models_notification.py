from django.db import models
from django.conf import settings
from generic.models import GenericIdEntity

class Notification(GenericIdEntity):
    NOTIFICATION_TYPES = (
        ('SALE_ADDED', 'Sale Added'),
        ('SYSTEM', 'System Notification'),
        ('profile_update', 'Profile Update'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES, default='SYSTEM')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.user}"
