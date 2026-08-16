

# Create your models here.
from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Activity(models.Model):

    ACTIVITY_TYPE_CHOICES = [
        ("email", "Email"),
        ("note", "Note"),
        ("call", "Call"),
        ("meeting", "Meeting"),
    ]

    activity_type = models.CharField(
        max_length=20,
        choices=ACTIVITY_TYPE_CHOICES
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="activities_created"
    )

    # Which CRM object does this activity belong to?
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
    )

    object_id = models.PositiveIntegerField()

    related_object = GenericForeignKey(
        "content_type",
        "object_id"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.activity_type} - {self.object_id}"