from rest_framework import serializers
from .models import Email


class EmailSerializer(serializers.ModelSerializer):

    sender_name = serializers.SerializerMethodField()
    sender_email = serializers.SerializerMethodField()

    recipient_name = serializers.SerializerMethodField()
    recipient_email = serializers.SerializerMethodField()

    date = serializers.SerializerMethodField()

    class Meta:
        model = Email

        fields = [
            "id",

            # Recipient
            "to_recipients",
            "recipient_name",
            "recipient_email",

            # Date
            "date",

            # Email
            "subject",
            "body",

            # Sender
            "sender_name",
            "sender_email",

            # CC / BCC
            "cc",
            "bcc",

            # Status
            "status",
            "sent_at",
            "error_message",
        ]

        extra_kwargs = {
            "to_recipients": {
                "write_only": True
            }
        }

        read_only_fields = [
            "id",
            "recipient_name",
            "recipient_email",
            "date",
            "sender_name",
            "sender_email",
            "status",
            "sent_at",
            "error_message",
        ]

    def get_sender_name(self, obj):
        user = obj.activity.created_by

        if user:
            return user.get_full_name() or user.email

        return None

    def get_sender_email(self, obj):
        user = obj.activity.created_by

        if user:
            return user.email

        return None

    def get_date(self, obj):
        return obj.activity.created_at

    def get_recipient_name(self, obj):
        recipients = obj.to_recipients

        if not recipients:
            return None

        recipient = recipients[0]

        if isinstance(recipient, dict):
            return recipient.get("name")

        return None

    def get_recipient_email(self, obj):
        recipients = obj.to_recipients

        if not recipients:
            return None

        recipient = recipients[0]

        if isinstance(recipient, dict):
            return recipient.get("email")

        return recipient