from django.contrib import admin

from .models import Deal


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):

    list_display = [
        "id",
        "deal_name",
        "lead_name",
        "deal_stage",
        "close_date",
        "deal_owner",
        "amount",
    ]

    list_filter = [
        "deal_owner",
        "deal_stage",
        "close_date",
        "created_date",
    ]

    search_fields = [
        "deal_name",
        "associated_lead__first_name",
        "associated_lead__last_name",
        "associated_lead__email",
    ]

    def lead_name(self, obj):
        return (
            f"{obj.associated_lead.first_name} "
            f"{obj.associated_lead.last_name}"
        ).strip()

    lead_name.short_description = "Lead"