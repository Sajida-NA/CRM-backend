from rest_framework import serializers

from .models import Meeting


class MeetingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Meeting

        fields = [
            "id",
            "title",
            "owner",
            "start_date",
            "start_time",
            "end_time",
            "attendees",
            "location",
            "reminder",
            "note",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]