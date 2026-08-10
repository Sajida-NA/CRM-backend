

# Register your models here.
from django.contrib import admin
from .models import Lead, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "phone_number",
        "job_title",
        "contact_owner",
        "lead_status",
        "company_type",
        "city",
    )

    list_filter = (
        "lead_status",
        "contact_owner",
        "company_type",
        "city",
    )

    search_fields = (
        "user__email",
        "user__first_name",
        "user__last_name",
        "phone_number",
    )