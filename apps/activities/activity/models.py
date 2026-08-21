# from django.conf import settings
# from django.db import models
# from django.contrib.contenttypes.fields import GenericForeignKey
# from django.contrib.contenttypes.models import ContentType


# class Activity(models.Model):

#     ACTIVITY_TYPE_CHOICES = [
#         ("email", "Email"),
#         ("note", "Note"),
#         ("call", "Call"),
#         ('task', 'Task'),
#         ("meeting", "Meeting"),
#     ]

#     # Type of activity
#     activity_type = models.CharField(
#         max_length=20,
#         choices=ACTIVITY_TYPE_CHOICES
#     )

#     # User/Admin who created the activity
#     created_by = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.SET_NULL,
#         null=True,
#         related_name="activities_created"
#     )

#     # CRM module this activity belongs to
#     # lead / deal / company / ticket
#     content_type = models.ForeignKey(
#         ContentType,
#         on_delete=models.CASCADE
#     )

#     # ID of the Lead/Deal/Company/Ticket
#     object_id = models.PositiveIntegerField()

#     # Gives access to the actual related object
#     related_object = GenericForeignKey(
#         "content_type",
#         "object_id"
#     )

#     created_at = models.DateTimeField(
#         auto_now_add=True
#     )

#     updated_at = models.DateTimeField(
#         auto_now=True
#     )

#     def __str__(self):
#         return f"{self.activity_type} - {self.object_id}"


from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Activity(models.Model):

    ACTIVITY_TYPE_CHOICES = [
        ("note", "Note"),
        ("call", "Call"),
        ("email", "Email"),
        ("meeting", "Meeting"),
        ("task", "Task"),
    ]

    # What type of activity is this?
    activity_type = models.CharField(
        max_length=20,
        choices=ACTIVITY_TYPE_CHOICES
    )

    # User who created the activity
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="activities"
    )

    # Generic relation to Lead / Deal / Company / Ticket
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
    )

    object_id = models.PositiveBigIntegerField()

    content_object = GenericForeignKey(
        "content_type",
        "object_id"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        indexes = [
            models.Index(
                fields=["content_type", "object_id"]
            ),
            models.Index(
                fields=["activity_type"]
            ),
        ]

    def __str__(self):
        return f"{self.activity_type} - {self.object_id}"