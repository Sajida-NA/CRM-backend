# Import Django admin tools
from django.contrib import admin

# Import Company model
from .models import Company


# ---------------------------------------------------------
# COMPANY ADMIN CONFIGURATION
# ---------------------------------------------------------

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):

    # Company table columns
    list_display = (
        "company_name",
        "company_owner",
        "phone_number",
        "industry",
        "city",
        "country_region",
        "created_date",
    )

    # Search fields
    search_fields = (
        "company_name",
        "domain_name",
        "email",
        "phone_number",
        "industry",
    )

    # Filters in Figma order
    list_filter = (
        "industry",
        "city",
        "country_region",
        "created_date",
    )