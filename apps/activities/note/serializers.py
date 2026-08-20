from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

from .models import Note
from apps.activities.activity.models import Activity


User = get_user_model()


class NoteSerializer(serializers.ModelSerializer):

    # ==========================================
    # INPUT FIELDS
    # ==========================================

    sender_id = serializers.IntegerField(
        write_only=True,
        required=True
    )

    module = serializers.CharField(
        write_only=True,
        required=True
    )

    module_id = serializers.IntegerField(
        write_only=True,
        required=True
    )

    # ==========================================
    # RESPONSE
    # ==========================================

    sender_name = serializers.SerializerMethodField()

    # ==========================================
    # META
    # ==========================================

    class Meta:

        model = Note

        fields = [
            "id",

            # Input only
            "sender_id",
            "module",
            "module_id",

            # Response
            "sender_name",

            # Note
            "note",

            # Timestamps
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "sender_name",
            "created_at",
            "updated_at",
        ]

    # ==========================================
    # SENDER NAME
    # ==========================================

    def get_sender_name(self, obj):

        user = obj.activity.created_by

        if not user:
            return None

        return (
            user.get_full_name()
            or user.email
        )

    # ==========================================
    # VALIDATE
    # ==========================================

    def validate(self, attrs):

        sender_id = attrs.pop(
            "sender_id",
            None
        )

        module = attrs.pop(
            "module",
            None
        )

        module_id = attrs.pop(
            "module_id",
            None
        )

        # ======================================
        # VALIDATE SENDER
        # ======================================

        if not sender_id:

            raise serializers.ValidationError({
                "sender_id": "This field is required."
            })

        try:

            sender = User.objects.get(
                id=sender_id
            )

        except User.DoesNotExist:

            raise serializers.ValidationError({
                "sender_id": (
                    f"User with id {sender_id} "
                    "does not exist."
                )
            })

        attrs["sender"] = sender

        # ======================================
        # VALIDATE MODULE
        # ======================================

        if not module:

            raise serializers.ValidationError({
                "module": "This field is required."
            })

        module = module.lower()

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

        if module not in MODULE_MAP:

            raise serializers.ValidationError({
                "module": (
                    "Invalid module. "
                    "Allowed modules: "
                    "lead, deal, company, ticket."
                )
            })

        app_label, model_name = MODULE_MAP[module]

        # ======================================
        # GET CONTENT TYPE
        # ======================================

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

        # ======================================
        # VALIDATE MODULE ID
        # ======================================

        if not module_id:

            raise serializers.ValidationError({
                "module_id": "This field is required."
            })

        model_class = content_type.model_class()

        if not model_class.objects.filter(
            id=module_id
        ).exists():

            raise serializers.ValidationError({
                "module_id": (
                    f"{module} with id "
                    f"{module_id} does not exist."
                )
            })

        # ======================================
        # STORE GENERIC RELATIONSHIP
        # ======================================

        attrs["content_type"] = content_type
        attrs["object_id"] = module_id

        return attrs

    # ==========================================
    # CREATE ACTIVITY + NOTE
    # ==========================================

    @transaction.atomic
    def create(self, validated_data):

        sender = validated_data.pop(
            "sender"
        )

        content_type = validated_data.pop(
            "content_type"
        )

        object_id = validated_data.pop(
            "object_id"
        )

        # Automatically create Activity
        activity = Activity.objects.create(
            activity_type="note",
            created_by=sender,
            content_type=content_type,
            object_id=object_id
        )

        # Create Note
        note = Note.objects.create(
            activity=activity,
            **validated_data
        )

        return note

    # ==========================================
    # REPRESENTATION
    # ==========================================

    def to_representation(self, instance):

        data = super().to_representation(instance)

        # Get related CRM object
        related_object = instance.activity.related_object

        if not related_object:
            return data

        module = instance.activity.content_type.model

        # ======================================
        # LEAD
        # ======================================

        if module == "lead":

            data["lead_name"] = (
                f"{related_object.first_name} "
                f"{related_object.last_name}"
            ).strip()

        # ======================================
        # DEAL
        # ======================================

        elif module == "deal":

            data["deal_name"] = getattr(
                related_object,
                "deal_name",
                None
            )

        # ======================================
        # COMPANY
        # ======================================

        elif module == "company":

            data["company_name"] = getattr(
                related_object,
                "name",
                None
            )

        # ======================================
        # TICKET
        # ======================================

        elif module == "ticket":

            data["ticket_name"] = getattr(
                related_object,
                "name",
                None
            )

        return data