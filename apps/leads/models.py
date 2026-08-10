from django.conf import settings
from django.db import models


class Product(models.Model):

    PRODUCT_CHOICES = [
        ("CRM Software", "CRM Software"),
        ("Marketing Tools", "Marketing Tools"),
        ("Analytics Tools", "Analytics Tools"),
    ]

    name = models.CharField(
        max_length=50,
        choices=PRODUCT_CHOICES,
        unique=True
    )

    def __str__(self):
        return self.name


class Lead(models.Model):

    CONTACT_OWNER_CHOICES = [
        ("Admin", "Admin"),
        ("Sales", "Sales"),
        ("Manager", "Manager"),
    ]

    LEAD_STATUS_CHOICES = [
        ("New", "New"),
        ("In Progress", "In Progress"),
        ("Closed", "Closed"),
        ("Open", "Open"),
    ]

    COMPANY_TYPE_CHOICES = [
        ("Startup", "Startup"),
        ("Enterprise", "Enterprise"),
        ("Private", "Private"),
        ("Public", "Public"),
    ]

    CITY_CHOICES = [
        ("Dubai", "Dubai"),
        ("Abu Dhabi", "Abu Dhabi"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="lead",
    )

    phone_number = models.CharField(
        max_length=20
    )

    job_title = models.CharField(
        max_length=100
    )

    contact_owner = models.CharField(
        max_length=20,
        choices=CONTACT_OWNER_CHOICES
    )

    lead_status = models.CharField(
        max_length=30,
        choices=LEAD_STATUS_CHOICES,
        default="New"
    )

    products = models.ManyToManyField(
        Product,
        blank=True,
        related_name="leads"
    )

    company_type = models.CharField(
        max_length=30,
        choices=COMPANY_TYPE_CHOICES
    )

    city = models.CharField(
        max_length=30,
        choices=CITY_CHOICES
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.user.email