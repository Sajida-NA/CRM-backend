from django.contrib import admin

# Register your models here.

from django.contrib import admin
from django.utils import timezone

from .models import Activity


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "activity_type",
        "object_id",
        "created_by",
        "created_at_local",
        "updated_at_local",
    )

    list_filter = (
        "activity_type",
        "created_at",
    )

    search_fields = (
        "activity_type",
        "created_by__email",
    )

    ordering = (
        "-created_at",
    )

    @admin.display(
        description="CREATED AT",
        ordering="created_at",
    )
    def created_at_local(self, obj):

        if not obj.created_at:
            return "-"

        local_time = timezone.localtime(
            obj.created_at,
            timezone.get_current_timezone(),
        )

        return local_time.strftime(
            "%b. %d, %Y, %I:%M %p"
        ).lstrip("0")

    @admin.display(
        description="UPDATED AT",
        ordering="updated_at",
    )
    def updated_at_local(self, obj):

        if not obj.updated_at:
            return "-"

        local_time = timezone.localtime(
            obj.updated_at,
            timezone.get_current_timezone(),
        )

        return local_time.strftime(
            "%b. %d, %Y, %I:%M %p"
        ).lstrip("0")

