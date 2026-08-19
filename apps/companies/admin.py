# Import Django admin tools
from django.contrib import admin

# Import Company model
from .models import Company


# ---------------------------------------------------------
# COMPANY ADMIN CONFIGURATION
# ---------------------------------------------------------

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):

    # ---------------------------------------------------------
    # COLUMNS DISPLAYED IN DJANGO ADMIN
    # ---------------------------------------------------------

    list_display = (
        "id",
        "company_name",
        "domain_name",
        "industry",
        "type",
        "company_owner",
        "city",
        "country_region",
        "no_of_employees",
        "annual_revenue",
        "phone_number",
        "email",
        "lifecycle_stage",
        "created_at",
    )

    # ---------------------------------------------------------
    # FIELDS USED FOR ADMIN SEARCH
    # ---------------------------------------------------------

    search_fields = (
        "company_name",
        "domain_name",
        "email",
        "phone_number",
        "industry",
    )

    # ---------------------------------------------------------
    # FILTER OPTIONS IN DJANGO ADMIN
    # ---------------------------------------------------------

    list_filter = (
        "industry",
        "type",
        "country_region",
        "lifecycle_stage",
    )