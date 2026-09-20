from rest_framework import serializers
from django.utils.html import strip_tags
from html import unescape

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

    # ==========================================
    # MODULE
    # ==========================================

    def get_module(self, obj):

        if not obj.content_type:
            return None

        return obj.content_type.model

    # ==========================================
    # CREATED BY NAME
    # ==========================================

    def get_created_by_name(self, obj):

        user = obj.created_by

        if not user:
            return None

        name = user.get_full_name()

        if name:
            return name

        return user.email

    # ==========================================
    # CLEAN HTML + HTML ENTITIES
    # ==========================================

    def get_plain_text(self, value):

        if not value:
            return ""

        text = strip_tags(value)

        text = unescape(text)

        text = text.replace("\xa0", " ")

        return " ".join(text.split())

    # ==========================================
    # ACTIVITY DATA
    # ==========================================

    def get_data(self, obj):

        # ==========================================
        # NOTE
        # ==========================================

        if obj.activity_type == "note":

            note = getattr(obj, "note", None)

            if not note:
                return None

            return {
                "id": note.id,

                # IMPORTANT:
                # Preserve rich-text HTML so formatting
                # like bold, italic, underline, lists, etc.
                # is available in Activity Timeline.
                "note": note.note or "",

                "created_at": note.created_at,
                "updated_at": note.updated_at,
            }

        # ==========================================
        # CALL
        # ==========================================

        if obj.activity_type == "call":

            call = getattr(obj, "call", None)

            if not call:
                return None

            return {
                "id": call.id,
                "call_outcome": call.call_outcome,
                "date": call.date,
                "time": call.time,
                "duration": call.duration,
                "note": self.get_plain_text(call.note),
                "created_at": call.created_at,
                "updated_at": call.updated_at,
            }

        # ==========================================
        # TASK
        # ==========================================

        if obj.activity_type == "task":

            task = getattr(obj, "task", None)

            if not task:
                return None

            return {
                "id": task.id,

                "task_name": task.task_name,

                "due_date": task.due_date,

                "time": task.time,

                "task_type": task.task_type,

                "priority": task.priority,

                # ManyToManyField
                "assigned_to": [
                    {
                        "id": user.id,
                        "name": (
                            user.get_full_name()
                            or user.email
                        ),
                    }
                    for user in task.assigned_to.all()
                ],

                "note": self.get_plain_text(
                    task.note
                ),

                "created_at": task.created_at,

                "updated_at": task.updated_at,
            }

        # ==========================================
        # EMAIL
        # ==========================================

        if obj.activity_type == "email":

            email = getattr(obj, "email", None)

            if not email:
                return None

            # --------------------------------------
            # Sender
            # --------------------------------------

            user = obj.created_by

            sender_name = None
            sender_email = None

            if user:

                sender_name = (
                    user.get_full_name()
                    or user.email
                )

                sender_email = user.email

            # --------------------------------------
            # Recipient
            # --------------------------------------

            recipient = None

            if email.to_recipients:

                recipient = email.to_recipients[0]

            return {
                "id": email.id,

                "subject": email.subject,

                "sender_name": sender_name,

                # "sender_email": sender_email,

                # "recipient_name": (
                #     recipient.get("name")
                #     if recipient
                #     else None
                # ),

                # "recipient_email": (
                #     recipient.get("email")
                #     if recipient
                #     else None
                # ),

                # "status": email.status,

                # "sent_at": email.sent_at,

                "created_at": obj.created_at,

                "updated_at": obj.updated_at,
            }

        # ==========================================
        # MEETING
        # ==========================================

        if obj.activity_type == "meeting":

            meeting = getattr(obj, "meeting", None)

            if not meeting:
                return None

            return {
                "id": meeting.id,
                "title": meeting.title,
                "start_date": meeting.start_date,
                "start_time": meeting.start_time,
                "end_time": meeting.end_time,
                "location": meeting.location,
                "reminder": meeting.reminder,
                "note": self.get_plain_text(meeting.note),
                "created_at": meeting.created_at,
                "updated_at": meeting.updated_at,
            }

        # ==========================================
        # UNKNOWN ACTIVITY
        # ==========================================

        return None
