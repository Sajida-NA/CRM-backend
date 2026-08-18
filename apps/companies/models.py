from django.db import models
from apps.accounts.models import User


LIFECYCLE_STAGE_CHOICES = [
    ("LEAD", "Lead"),
    ("PROSPECT", "Prospect"),
    ("CUSTOMER", "Customer"),
    ("LOST", "Lost"),
]


class Company(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    website = models.URLField(blank=True, null=True)

    industry = models.CharField(max_length=100)
    employees = models.PositiveIntegerField(default=0)

    annual_revenue = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
    )

    lifecycle_stage = models.CharField(
        max_length=20,
        choices=LIFECYCLE_STAGE_CHOICES,
        default="LEAD",
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="companies",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
     return self.name

    class Meta:
        db_table = "companies"
        ordering = ["-created_at"]



    