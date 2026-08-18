from django.db import models

from apps.accounts.models import User


class Ticket(models.Model):
    STATUS_CHOICES = [
        ("NEW", "New"),
        ("OPEN", "Open"),
        ("IN_PROGRESS", "In Progress"),
        ("WAITING_ON_CONTACT", "Waiting on Contact"),
        ("WAITING_ON_US", "Waiting on Us"),
        ("CLOSED", "Closed"),
    ]

    SOURCE_CHOICES = [
        ("CHAT", "Chat"),
        ("EMAIL", "Email"),
        ("PHONE", "Phone"),
        ("WEB", "Web"),
    ]

    PRIORITY_CHOICES = [
        ("LOW", "Low"),
        ("MEDIUM", "Medium"),
        ("HIGH", "High"),
        ("CRITICAL", "Critical"),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="NEW")
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default="WEB")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default="MEDIUM")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tickets")
    associated_deal = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tickets"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
