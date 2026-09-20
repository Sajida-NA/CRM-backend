from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Call


@admin.register(Call)
class CallAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "activity",
        "connected",
        "call_mode",
        "call_outcome",
        "twilio_status",
        "date",
        "time",
        "duration",
        "created_at",
    )

    list_filter = (
        "call_mode",
        "call_outcome",
        "twilio_status",
        "date",
    )

    search_fields = (
        "twilio_call_sid",
        "user_twilio_call_sid",
        "customer_twilio_call_sid",
        "note",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "twilio_call_sid",
        "user_twilio_call_sid",
        "customer_twilio_call_sid",
        "twilio_status",
        "duration",
    )

    ordering = ("-created_at",)