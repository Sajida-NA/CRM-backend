from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Activity(models.Model):

    ACTIVITY_TYPES = [
        ("NOTE", "Note"),
        ("EMAIL", "Email"),
        ("CALL", "Call"),
        ("TASK", "Task"),
        ("MEETING", "Meeting"),
    ]

    activity_type = models.CharField(
        max_length=20,
        choices=ACTIVITY_TYPES,
    )

    subject = models.CharField(
        max_length=255,
    )

    description = models.TextField(
        blank=True,
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    content_type = models.ForeignKey(
    ContentType,
    on_delete=models.CASCADE,
    null=True,
    blank=True,

    )
    

    object_id = models.PositiveIntegerField(
    null=True,
    blank=True,
    )

    content_object = GenericForeignKey(
        "content_type",
        "object_id",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.subject