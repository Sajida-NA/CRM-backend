from rest_framework import serializers

from .models import Email


class EmailSerializer(serializers.ModelSerializer):

    # -----------------------------------
    # Sender
    # -----------------------------------

    sender_id = serializers.SerializerMethodField()
    sender_name = serializers.SerializerMethodField()
    sender_email = serializers.SerializerMethodField()

    # -----------------------------------
    # Recipient
    # -----------------------------------

    recipient_id = serializers.SerializerMethodField()
    recipient_name = serializers.SerializerMethodField()
    recipient_email = serializers.SerializerMethodField()

    # -----------------------------------
    # Date
    # -----------------------------------

    date = serializers.SerializerMethodField()

    class Meta:
        model = Email

        fields = [
            "id",

            # Sender
            "sender_id",
            "sender_name",
            "sender_email",

            # Recipient
            "recipient_id",
            "recipient_name",
            "recipient_email",

            # Email
            "cc",
            "bcc",
            "subject",
            "body",

            # Status
            "date",
            "sent_at",
            "status",
            "error_message",
        ]

        read_only_fields = [
            "id",

            "sender_id",
            "sender_name",
            "sender_email",

            "recipient_id",
            "recipient_name",
            "recipient_email",

            "date",
            "sent_at",
            "status",
            "error_message",
        ]

    # ===================================
    # Sender
    # ===================================

    def get_sender_id(self, obj):

        user = obj.activity.created_by

        if not user:
            return None

        return user.id

    def get_sender_name(self, obj):

        user = obj.activity.created_by

        if not user:
            return None

        return user.get_full_name() or user.email

    def get_sender_email(self, obj):

        user = obj.activity.created_by

        if not user:
            return None

        return user.email

    # ===================================
    # Recipient
    # ===================================

    def _get_first_recipient(self, obj):

        recipients = obj.to_recipients

        if not recipients:
            return None

        return recipients[0]

    def get_recipient_id(self, obj):

        recipient = self._get_first_recipient(obj)

        if not recipient:
            return None

        return recipient.get("id")

    def get_recipient_name(self, obj):

        recipient = self._get_first_recipient(obj)

        if not recipient:
            return None

        return recipient.get("name")

    def get_recipient_email(self, obj):

        recipient = self._get_first_recipient(obj)

        if not recipient:
            return None

        return recipient.get("email")

    # ===================================
    # Date
    # ===================================

    def get_date(self, obj):

        return obj.activity.created_at