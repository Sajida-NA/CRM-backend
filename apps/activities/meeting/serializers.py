from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from .models import Meeting


User = get_user_model()


# =========================================================
# CREATE / UPDATE SERIALIZER
# =========================================================

class MeetingSerializer(serializers.ModelSerializer):

    # -----------------------------------------
    # INPUT ONLY
    # -----------------------------------------

    sender_id = serializers.IntegerField(
        write_only=True
    )

    module = serializers.CharField(
        write_only=True
    )

    module_id = serializers.IntegerField(
        write_only=True
    )

    class Meta:

        model = Meeting

        fields = [
            "id",

            # Input
            "sender_id",
            "module",
            "module_id",

            # Meeting
            "title",
            "owner",
            "start_date",
            "start_time",
            "end_time",
            "attendees",
            "location",
            "reminder",
            "note",

            # Timestamps
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "owner",
            "created_at",
            "updated_at",
        ]

    # =====================================================
    # VALIDATE
    # =====================================================

    def validate(self, attrs):

        # -----------------------------------------
        # Get input values
        # -----------------------------------------

        sender_id = attrs.pop(
            "sender_id"
        )

        module = attrs.pop(
            "module"
        )

        module_id = attrs.pop(
            "module_id"
        )

        # -----------------------------------------
        # Validate sender
        # -----------------------------------------

        try:

            sender = User.objects.get(
                id=sender_id
            )

        except User.DoesNotExist:

            raise serializers.ValidationError({
                "sender_id": "Sender does not exist."
            })

        # -----------------------------------------
        # Allowed modules
        # -----------------------------------------

        MODULE_MAP = {

            "lead": (
                "leads",
                "lead"
            ),

            "deal": (
                "deals",
                "deal"
            ),

            "company": (
                "companies",
                "company"
            ),

            "ticket": (
                "tickets",
                "ticket"
            ),
        }

        module = module.lower()

        # -----------------------------------------
        # Validate module name
        # -----------------------------------------

        if module not in MODULE_MAP:

            raise serializers.ValidationError({
                "module": (
                    "Invalid module. "
                    "Allowed modules: "
                    "lead, deal, company, ticket."
                )
            })

        app_label, model_name = MODULE_MAP[
            module
        ]

        # -----------------------------------------
        # Get ContentType
        # -----------------------------------------

        try:

            content_type = ContentType.objects.get(
                app_label=app_label,
                model=model_name
            )

        except ContentType.DoesNotExist:

            raise serializers.ValidationError({
                "module": (
                    f"{module} module does not exist."
                )
            })

        # -----------------------------------------
        # Get CRM object
        # -----------------------------------------

        model_class = content_type.model_class()

        try:

            related_object = model_class.objects.get(
                id=module_id
            )

        except model_class.DoesNotExist:

            raise serializers.ValidationError({
                "module_id": (
                    f"{module} with id "
                    f"{module_id} does not exist."
                )
            })

        # -----------------------------------------
        # Store internal values
        # -----------------------------------------

        attrs["_sender"] = sender

        attrs["content_type"] = content_type

        attrs["object_id"] = module_id

        attrs["_module"] = module

        attrs["_related_object"] = related_object

        return attrs

    # =====================================================
    # CREATE
    # =====================================================

    def create(self, validated_data):

        # -----------------------------------------
        # Get internal values
        # -----------------------------------------

        sender = validated_data.pop(
            "_sender"
        )

        validated_data.pop(
            "_module"
        )

        validated_data.pop(
            "_related_object"
        )

        # -----------------------------------------
        # IMPORTANT:
        # Remove attendees before Meeting.objects.create()
        # -----------------------------------------

        attendees = validated_data.pop(
            "attendees",
            []
        )

        # -----------------------------------------
        # Sender becomes meeting creator/owner
        # -----------------------------------------

        validated_data["owner"] = sender

        # -----------------------------------------
        # Create meeting
        # -----------------------------------------

        meeting = Meeting.objects.create(
            **validated_data
        )

        # -----------------------------------------
        # Add attendees AFTER meeting is created
        # -----------------------------------------

        if attendees:

            meeting.attendees.set(
                attendees
            )

        return meeting


# =========================================================
# RESPONSE SERIALIZER
# =========================================================

class MeetingResponseSerializer(
    serializers.ModelSerializer
):

    created_by = serializers.SerializerMethodField()

    module = serializers.SerializerMethodField()

    lead = serializers.SerializerMethodField()

    attendees = serializers.SerializerMethodField()

    class Meta:

        model = Meeting

        fields = [
            "id",
            "created_by",
            "module",
            "lead",
            "title",
            "start_date",
            "start_time",
            "end_time",
            "attendees",
            "location",
            "reminder",
            "note",
        ]

    # =====================================================
    # CREATED BY
    # =====================================================

    def get_created_by(self, obj):

        if not obj.owner:
            return None

        return {
            "id": obj.owner.id,

            "name": (
                obj.owner.get_full_name()
                or obj.owner.email
            )
        }

    # =====================================================
    # MODULE
    # =====================================================

    def get_module(self, obj):

        if not obj.content_type:
            return None

        return obj.content_type.model

    # =====================================================
    # LEAD / DEAL / COMPANY / TICKET
    # =====================================================

    def get_lead(self, obj):

        related_object = obj.related_object

        if not related_object:
            return None

        model_name = obj.content_type.model

        # -----------------------------------------
        # LEAD
        # -----------------------------------------

        if model_name == "lead":

            return {
                "id": related_object.id,

                "name": (
                    f"{related_object.first_name} "
                    f"{related_object.last_name}"
                ).strip()
            }

        # -----------------------------------------
        # DEAL
        # -----------------------------------------

        if model_name == "deal":

            lead = getattr(
                related_object,
                "associated_lead",
                None
            )

            if lead:

                return {
                    "id": lead.id,

                    "name": (
                        f"{lead.first_name} "
                        f"{lead.last_name}"
                    ).strip()
                }

            return {
                "id": related_object.id,

                "name": getattr(
                    related_object,
                    "deal_name",
                    str(related_object)
                )
            }

        # -----------------------------------------
        # COMPANY
        # -----------------------------------------

        if model_name == "company":

            return {
                "id": related_object.id,

                "name": getattr(
                    related_object,
                    "name",
                    str(related_object)
                )
            }

        # -----------------------------------------
        # TICKET
        # -----------------------------------------

        if model_name == "ticket":

            return {
                "id": related_object.id,

                "name": getattr(
                    related_object,
                    "name",
                    str(related_object)
                )
            }

        return None

    # =====================================================
    # ATTENDEES
    # =====================================================

    def get_attendees(self, obj):

        return [
            {
                "id": user.id,

                "name": (
                    user.get_full_name()
                    or user.email
                )
            }

            for user in obj.attendees.all()
        ]