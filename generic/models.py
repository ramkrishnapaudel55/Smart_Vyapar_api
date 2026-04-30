import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone


def generate_reference_id():
    return uuid.uuid4()


class GenericEntity(models.Model):
    id = models.AutoField(primary_key=True)
    reference_id = models.UUIDField(default=generate_reference_id, unique=True, editable=False)

    class Meta:
        abstract = True


class GenericIdEntity(GenericEntity):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="%(class)s_created",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="%(class)s_updated",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    updated_at = models.DateTimeField(default=timezone.now)

    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="%(class)s_approved",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    approved_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


