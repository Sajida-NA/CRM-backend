

# Register your models here.
from django.contrib import admin

from .models import Deal


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):

    list_display = [
        "id",
        "deal_name",
        "associated_lead",
        "deal_owner",
        "deal_stage",
        "amount",
        "close_date",
        "priority",
    ]

    list_filter = [
        "deal_stage",
        "priority",
    ]

    search_fields = [
        "deal_name",
        "associated_lead__first_name",
        "associated_lead__last_name",
        "deal_owner__first_name",
        "deal_owner__last_name",
    ]