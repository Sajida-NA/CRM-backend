from django.contrib import admin

from .models import Meeting


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "title",
        "owner",
        "start_date",
        "start_time",
        "created_at",
    )

    list_filter = (
        "start_date",
        "reminder",
    )

    search_fields = (
        "title",
        "location",
        "note",
        "owner__email",
        "owner__first_name",
        "owner__last_name",
    )