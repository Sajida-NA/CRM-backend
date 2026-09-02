# from django.conf import settings
# from django.db import models
# from django.contrib.contenttypes.fields import GenericForeignKey
# from django.contrib.contenttypes.models import ContentType

# from apps.activities.activity.models import Activity


# class Task(models.Model):

#     TASK_TYPE_CHOICES = [
#         ("follow_up", "Follow Up"),
#         ("call", "Call"),
#         ("meeting", "Meeting"),
#         ("email", "Email"),
#         ("other", "Other"),
#     ]

#     PRIORITY_CHOICES = [
#         ("low", "Low"),
#         ("medium", "Medium"),
#         ("high", "High"),
#     ]

#     # Activity automatically created for this task
#     activity = models.OneToOneField(
#         Activity,
#         on_delete=models.CASCADE,
#         related_name="task"
#     )

#     # -------------------------
#     # Task details
#     # -------------------------

#     task_name = models.CharField(
#         max_length=255
#     )

#     due_date = models.DateField()

#     time = models.TimeField()

#     task_type = models.CharField(
#         max_length=30,
#         choices=TASK_TYPE_CHOICES
#     )

#     priority = models.CharField(
#         max_length=20,
#         choices=PRIORITY_CHOICES
#     )

#     # -------------------------
#     # Assigned user
#     # -------------------------

#     assigned_to = models.ForeignKey(
#             settings.AUTH_USER_MODEL,
#             on_delete=models.SET_NULL,
#             null=True,
#             related_name="assigned_tasks"
#         )

#     note = models.TextField()

    

    

#     # -------------------------
#     # CRM module
#     # Lead / Deal / Company / Ticket
#     # -------------------------

#     content_type = models.ForeignKey(
#         ContentType,
#         on_delete=models.CASCADE
#     )

#     object_id = models.PositiveIntegerField()

#     related_object = GenericForeignKey(
#         "content_type",
#         "object_id"
#     )

#     # -------------------------
#     # Timestamps
#     # -------------------------

#     created_at = models.DateTimeField(
#         auto_now_add=True
#     )

#     updated_at = models.DateTimeField(
#         auto_now=True
#     )

#     def __str__(self):
#         return self.task_name




from django.conf import settings
from django.db import models

from apps.activities.activity.models import Activity


class Task(models.Model):

    TASK_TYPE_CHOICES = [
        ("follow_up", "Follow Up"),
        ("call", "Call"),
        ("meeting", "Meeting"),
        ("email", "Email"),
        ("other", "Other"),
    ]

    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]

    # -------------------------
    # Activity
    # -------------------------

    activity = models.OneToOneField(
        Activity,
        on_delete=models.CASCADE,
        related_name="task"
    )

    # -------------------------
    # Task details
    # -------------------------

    task_name = models.CharField(
        max_length=255
    )

    due_date = models.DateField()

    time = models.TimeField()

    task_type = models.CharField(
        max_length=30,
        choices=TASK_TYPE_CHOICES
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES
    )

    # -------------------------
    # Assigned user
    # -------------------------

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="assigned_tasks"
    )

    note = models.TextField()

    # -------------------------
    # Timestamps
    # -------------------------

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.task_name