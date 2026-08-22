from rest_framework import serializers

from .models import Activity


class ActivitySerializer(serializers.ModelSerializer):

    module = serializers.SerializerMethodField()

    module_id = serializers.IntegerField(
        source="object_id",
        read_only=True
    )

    created_by_name = serializers.SerializerMethodField()

    data = serializers.SerializerMethodField()

    class Meta:
        model = Activity

        fields = [
            "id",
            "activity_type",
            "module",
            "module_id",
            "created_by",
            "created_by_name",
            "created_at",
            "updated_at",
            "data",
        ]

        read_only_fields = [
            "id",
            "created_by",
            "created_by_name",
            "created_at",
            "updated_at",
        ]

    def get_module(self, obj):

        return obj.content_type.model

    def get_created_by_name(self, obj):

        user = obj.created_by

        if hasattr(user, "get_full_name"):
            name = user.get_full_name()

            if name:
                return name

        return user.email

    def get_data(self, obj):

        if obj.activity_type == "note":

            return {
                "id": obj.note.id,
                "content": obj.note.content,
                "created_at": obj.note.created_at,
                "updated_at": obj.note.updated_at,
            }

        if obj.activity_type == "call":

            return {
                "id": obj.call.id,
                "call_outcome": obj.call.call_outcome,
                "duration": obj.call.duration,
                "notes": obj.call.notes,
                "created_at": obj.call.created_at,
                "updated_at": obj.call.updated_at,
            }

        if obj.activity_type == "task":

            return {
                "id": obj.task.id,
                "title": obj.task.title,
                "description": obj.task.description,
                "due_date": obj.task.due_date,
                "status": obj.task.status,
                "priority": obj.task.priority,
                "created_at": obj.task.created_at,
                "updated_at": obj.task.updated_at,
            }

        if obj.activity_type == "email":

            return {
                "id": obj.email.id,
                "to_recipients": obj.email.to_recipients,
                "cc": obj.email.cc,
                "bcc": obj.email.bcc,
                "subject": obj.email.subject,
                "body": obj.email.body,
                "status": obj.email.status,
                "sent_at": obj.email.sent_at,
            }

        if obj.activity_type == "meeting":

            return {
                "id": obj.meeting.id,
                "title": obj.meeting.title,
                "meeting_date": obj.meeting.meeting_date,
                "location": obj.meeting.location,
                "description": obj.meeting.description,
                "reminder": obj.meeting.reminder,
                "created_at": obj.meeting.created_at,
                "updated_at": obj.meeting.updated_at,
            }

        return None