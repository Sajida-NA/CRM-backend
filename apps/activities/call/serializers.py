from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

from .models import Call
from apps.activities.activity.models import Activity


User = get_user_model()


class CallSerializer(serializers.ModelSerializer):

    # ---------------------------------------------
    # INPUT FIELDS
    # ---------------------------------------------

    module = serializers.CharField(write_only=True)
    module_id = serializers.IntegerField(write_only=True)
    sender_id = serializers.IntegerField(write_only=True)

    # ---------------------------------------------
    # OUTPUT FIELDS
    # ---------------------------------------------

    sender = serializers.SerializerMethodField(read_only=True)

    connected = serializers.SerializerMethodField(
        read_only=True
    )

    class Meta:
        model = Call

        fields = [
            "id",

            # Sender - output only name
            "sender",

            # Input only
            "module",
            "module_id",
            "sender_id",

            # Connected CRM object
            "connected",

            # Call details
            "call_outcome",
            "date",
            "time",
            "note",

            # Timestamps
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "sender",
            "connected",
            "created_at",
            "updated_at",
        ]

    # =================================================
    # VALIDATION
    # =================================================

    def validate(self, attrs):

        module = attrs.get("module")
        module_id = attrs.get("module_id")
        sender_id = attrs.get("sender_id")

        allowed_modules = [
            "lead",
            "deal",
            "company",
            "ticket",
        ]

        if module not in allowed_modules:
            raise serializers.ValidationError({
                "module": (
                    "Invalid module. Allowed modules are: "
                    "lead, deal, company, ticket."
                )
            })

        try:
            content_type = ContentType.objects.get(
                model=module
            )
        except ContentType.DoesNotExist:
            raise serializers.ValidationError({
                "module": f"Model '{module}' does not exist."
            })

        model_class = content_type.model_class()

        if not model_class.objects.filter(
            pk=module_id
        ).exists():
            raise serializers.ValidationError({
                "module_id": (
                    f"{module} with id {module_id} "
                    "does not exist."
                )
            })

        if not User.objects.filter(
            pk=sender_id
        ).exists():
            raise serializers.ValidationError({
                "sender_id": (
                    f"User with id {sender_id} "
                    "does not exist."
                )
            })

        return attrs

    # =================================================
    # CREATE CALL + ACTIVITY
    # =================================================

    def create(self, validated_data):

        module = validated_data.pop("module")
        module_id = validated_data.pop("module_id")
        sender_id = validated_data.pop("sender_id")

        content_type = ContentType.objects.get(
            model=module
        )

        # Automatically create Activity
        activity = Activity.objects.create(
            activity_type="call",
            created_by_id=sender_id,
            content_type=content_type,
            object_id=module_id,
        )

        # Create Call
        call = Call.objects.create(
            activity=activity,
            connected_content_type=content_type,
            connected_object_id=module_id,
            **validated_data
        )

        return call

    # =================================================
    # SENDER NAME
    # =================================================

    def get_sender(self, obj):

        user = obj.activity.created_by

        if not user:
            return None

        return user.get_full_name() or user.email

    # =================================================
    # CONNECTED OBJECT NAME
    # =================================================

    def get_connected(self, obj):

        connected_object = obj.connected

        if not connected_object:
            return None

        # ---------------------------------------------
        # Lead
        # ---------------------------------------------

        if hasattr(
            connected_object,
            "first_name"
        ):

            first_name = (
                connected_object.first_name or ""
            )

            last_name = getattr(
                connected_object,
                "last_name",
                ""
            ) or ""

            return (
                f"{first_name} {last_name}"
            ).strip()

        # ---------------------------------------------
        # Deal
        # ---------------------------------------------

        if hasattr(
            connected_object,
            "deal_name"
        ):
            return connected_object.deal_name

        # ---------------------------------------------
        # Company
        # ---------------------------------------------

        if hasattr(
            connected_object,
            "company_name"
        ):
            return connected_object.company_name

        # ---------------------------------------------
        # Ticket
        # ---------------------------------------------

        if hasattr(
            connected_object,
            "title"
        ):
            return connected_object.title

        # ---------------------------------------------
        # Fallback
        # ---------------------------------------------

        return str(connected_object)