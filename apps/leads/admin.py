from django.contrib import admin

from .models import Lead, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "created_at",
    )

    search_fields = (
        "name",
    )


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "contact_owner",
        "lead_status",
        "company_type",
        "city",
        "created_at",
    )

    list_filter = (
        "lead_status",
        "company_type",
        "city",
        "contact_owner",
        "created_at",
    )

    search_fields = (
        "first_name",
        "last_name",
        "email",
        "phone_number",
    )