


from django.conf import settings 
from django.db import models 
 
from apps.companies.models import Company 
 
 
class Product(models.Model): 
 
    name = models.CharField( 
        max_length=100, 
        unique=True 
    ) 
 
    description = models.TextField( 
        blank=True, 
        null=True 
    ) 
 
    created_at = models.DateTimeField( 
        auto_now_add=True 
    ) 
 
    def __str__(self): 
        return self.name 
 

class Lead(models.Model):

    STATUS_CHOICES = [
        ("New", "New"),
        ("Open", "Open"),
        ("In Progress", "In Progress"),
        ("Converted", "Converted"),
    ]

    email = models.EmailField(
        unique=True
    )

    first_name = models.CharField(
        max_length=100
    )

    last_name = models.CharField(
        max_length=100
    )

    phone_number = models.CharField(
        max_length=20
    )

    job_title = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    contact_owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_leads"
    )

    lead_status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="New"
    )

    products = models.ManyToManyField(
        Product,
        related_name="leads",
        blank=True
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="company_leads"
    )

    city = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    created_date = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"