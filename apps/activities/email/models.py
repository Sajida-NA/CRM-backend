from django.db import models

from apps.activities.activity.models import Activity


class Email(models.Model):

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("sent", "Sent"),
        ("failed", "Failed"),
    ]

    activity = models.OneToOneField(
        Activity,
        on_delete=models.CASCADE,
        related_name="email"
    )

    to_recipients = models.JSONField(
        default=list
    )

    cc = models.JSONField(
        default=list,
        blank=True
    )

    bcc = models.JSONField(
        default=list,
        blank=True
    )

    subject = models.CharField(
        max_length=255,
        blank=True
    )

    body = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="sent"
    )

    sent_at = models.DateTimeField(
        null=True,
        blank=True
    )

    error_message = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return self.subject or "No Subject"