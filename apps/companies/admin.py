from django.contrib import admin

from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):

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

    search_fields = (
        "company_name",
        "domain_name",
        "email",
        "phone_number",
        "industry",
    )

    list_filter = (
        "industry",
        "type",
        "country_region",
        "lifecycle_stage",
    )