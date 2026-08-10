from django.contrib import admin
from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "email",
        "phone_number",
        "industry",
        "owner",
        "lifecycle_stage",
        "created_at",
    )

    search_fields = (
        "name",
        "email",
        "phone_number",
    )

    list_filter = (
        "industry",
        "lifecycle_stage",
    )

# Register your models here.
