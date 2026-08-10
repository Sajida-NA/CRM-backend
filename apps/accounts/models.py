from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager

class User(AbstractUser):
    username = None
    
    INDUSTRY_CHOICES =  [("IT", "IT"),
                         ("Finance", "Finance"),
                         ("Healthcare", "Healthcare"),
                         ("Education", "Education"),
                         ("Manufacturing", "Manufacturing"),
                         ("Retail", "Retail"), ("Other", "Other"),
                        ]
     

    email = models.EmailField(unique=True)

    first_name = models.CharField(
        max_length=150
    )

    last_name = models.CharField(
        max_length=150
    )

    # when normal user becomes a lead user ,the value of is_lead=true
    is_lead = models.BooleanField(default=False) 

    phone_number = models.CharField( max_length=15,unique=True)

    company_name = models.CharField(max_length=255)
    
    industry_type = models.CharField( max_length=50, choices=INDUSTRY_CHOICES )
    
    country = models.CharField(max_length=100)

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []
    
    objects = UserManager()

    def __str__(self):
        return self.email