from django.db import models

from apps.activities.activity.models import Activity


class Email(models.Model):

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("sent", "Sent"),
        ("failed", "Failed"),
    ]

    # One Activity = One Email
    activity = models.OneToOneField(
        Activity,
        on_delete=models.CASCADE,
        related_name="email"
    )

    # Recipient information
    #
    # Example:
    #
    # [
    #     {
    #         "id": 3,
    #         "name": "Sonu Smith",
    #         "email": "sonu@example.com"
    #     }
    # ]
    #
    to_recipients = models.JSONField(
        default=list
    )

    # CC recipients
    cc = models.JSONField(
        default=list,
        blank=True
    )

    # BCC recipients
    bcc = models.JSONField(
        default=list,
        blank=True
    )

    # Email subject
    subject = models.CharField(
        max_length=255,
        blank=True
    )

    # Email body
    body = models.TextField(
        blank=True
    )

    # Sending status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft"
    )

    # When email was successfully sent
    sent_at = models.DateTimeField(
        null=True,
        blank=True
    )

    # Error information if sending fails
    error_message = models.TextField(
        null=True,
        blank=True
    )

    def __str__(self):

        return self.subject or "No Subject"