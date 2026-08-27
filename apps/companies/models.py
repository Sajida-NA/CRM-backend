# Import Django model tools
from django.db import models

# Import custom User model
from apps.accounts.models import User


# ---------------------------------------------------------
# COMPANY MODEL
# ---------------------------------------------------------

class Company(models.Model):

    # Domain Name / Company Website
    domain_name = models.URLField(
        max_length=255,
        blank=True,
        null=True,
    )

    # Company Name
    company_name = models.CharField(
        max_length=255,
    )

    # Company Owner
    company_owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="companies",
    )

    # Industry
    industry = models.CharField(
        max_length=100,
    )

    # Company Type
    type = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    # City
    city = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    # Country / Region
    country_region = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    # Number of Employees
    no_of_employees = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    # Annual Revenue
    annual_revenue = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
    )

    # Phone Number
    phone_number = models.CharField(
        max_length=20,
        unique=True,
    )

    # Company Email
    email = models.EmailField(
        unique=True,
    )

    # Created Date
    created_date = models.DateTimeField(
        auto_now_add=True,
    )

    # Updated Date
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    # Return Company Name
    def __str__(self):
        return self.company_name

    # ---------------------------------------------------------
    # MODEL METADATA
    # ---------------------------------------------------------

    class Meta:
        db_table = "companies"
        ordering = ["-created_date"]