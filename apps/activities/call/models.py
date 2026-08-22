from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from apps.activities.activity.models import Activity


class Call(models.Model):

    CALL_OUTCOME_CHOICES = [
        ("connected", "Connected"),
        ("no_answer", "No Answer"),
        ("busy", "Busy"),
        ("left_voicemail", "Left Voicemail"),
        ("wrong_number", "Wrong Number"),
        ("callback_requested", "Callback Requested"),
        ("not_interested", "Not Interested"),
        ("other", "Other"),
    ]

    # Link Call to the base Activity
    activity = models.OneToOneField(
        Activity,
        on_delete=models.CASCADE,
        related_name="call"
    )

    # -------------------------------------------------
    # Connected CRM object
    # -------------------------------------------------

    connected_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name="connected_calls"
    )

    connected_object_id = models.PositiveBigIntegerField()

    connected = GenericForeignKey(
        "connected_content_type",
        "connected_object_id"
    )

    # -------------------------------------------------
    # Call details
    # -------------------------------------------------

    call_outcome = models.CharField(
        max_length=50,
        choices=CALL_OUTCOME_CHOICES
    )

    date = models.DateField()

    time = models.TimeField()

    # -------------------------------------------------
    # Note
    # -------------------------------------------------

    note = models.TextField()

    # -------------------------------------------------
    # Timestamps
    # -------------------------------------------------

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Call - {self.date} {self.time}"