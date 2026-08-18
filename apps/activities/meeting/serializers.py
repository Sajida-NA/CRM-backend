from rest_framework import serializers
from .models import Meeting


class MeetingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Meeting

        fields = [
            "id",
            "title",
            "owner",
            "related_module",
            "record_id",
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