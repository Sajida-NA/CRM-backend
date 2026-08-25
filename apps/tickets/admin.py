# tickets/admin.py

from django.contrib import admin
from .models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        "ticket_name",
        "associated_deal",
        "ticket_status",
        "priority",
        "source",
        "ticket_owner",
        "created_date",
    )

    list_filter = (
        "ticket_owner",
        "ticket_status",
        "source",
        "priority",
        "created_date"
        
    )

    search_fields = (
        "ticket_name",
        "description",
    )