from django.contrib import admin

from .models import Meeting


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "title",
        "owner",
        "content_type",
        "object_id",
        "start_date",
        "start_time",
        "created_at",
    )

    list_filter = (
        "content_type",
        "start_date",
    )

    search_fields = (
        "title",
        "location",
        "note",
    )