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
       
        "lead_status",
       
        "created_date",
    )

    list_filter = (
        "lead_status",
        "created_date",
    )

    search_fields = (
        "email",
        "phone_number",
        "first_name",
        "last_name",
    )