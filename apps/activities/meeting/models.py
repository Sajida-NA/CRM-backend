



from django.db import models
from django.conf import settings

from apps.activities.activity.models import Activity


class Meeting(models.Model):

    REMINDER_CHOICES = [
        ("5_MIN", "5 minutes before"),
        ("15_MIN", "15 minutes before"),
        ("30_MIN", "30 minutes before"),
        ("1_HOUR", "1 hour before"),
        ("1_DAY", "1 day before"),
    ]

    # ========================================
    # ACTIVITY
    # ========================================

    activity = models.OneToOneField(
        Activity,
        on_delete=models.CASCADE,
        related_name="meeting",
        null=True,
        blank=True,
    )

    # ========================================
    # MEETING DETAILS
    # ========================================

    title = models.CharField(
        max_length=255
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_meetings"
    )

    start_date = models.DateField()

    start_time = models.TimeField()

    end_time = models.TimeField()

    attendees = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="meeting_attendees",
        blank=True
    )

    location = models.CharField(
        max_length=255
    )

    reminder = models.CharField(
        max_length=20,
        choices=REMINDER_CHOICES,
        blank=True,
        null=True
    )

    note = models.TextField(
        blank=True,
        default=""
    )

    # ========================================
    # TIMESTAMPS
    # ========================================

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.title
