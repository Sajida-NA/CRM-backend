


from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db import transaction

from rest_framework import serializers

from .models import Meeting
from apps.activities.activity.models import Activity


User = get_user_model()


# ============================================================
# CREATE / UPDATE MEETING SERIALIZER
# ============================================================

class MeetingSerializer(serializers.ModelSerializer):

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

    class Meta:
        model = Meeting

        fields = [
            "id",
            "sender_id",
            "module",
            "module_id",
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

    # ========================================================
    # SUPPORTED MODULES
    # ========================================================

    MODULE_MAP = {
        "lead": ("leads", "lead"),
        "deal": ("deals", "deal"),
        "company": ("companies", "company"),
        "ticket": ("tickets", "ticket"),
    }

    # ========================================================
    # VALIDATE
    # ========================================================

    def validate(self, attrs):

        sender_id = attrs.get("sender_id")
        module = attrs.get("module")
        module_id = attrs.get("module_id")

        # ----------------------------------------------------
        # Validate sender
        # ----------------------------------------------------

        try:
            sender = User.objects.get(id=sender_id)
        except User.DoesNotExist:
            raise serializers.ValidationError({
                "sender_id": "User does not exist."
            })

        # ----------------------------------------------------
        # Validate module
        # ----------------------------------------------------

        module = module.lower().strip()

        if module not in self.MODULE_MAP:
            raise serializers.ValidationError({
                "module": (
                    "Invalid module. "
                    "Allowed values are: "
                    "lead, deal, company, ticket."
                )
            })

        app_label, model_name = self.MODULE_MAP[module]

        # ----------------------------------------------------
        # Get ContentType
        # ----------------------------------------------------

        try:
            content_type = ContentType.objects.get(
                app_label=app_label,
                model=model_name
            )
        except ContentType.DoesNotExist:
            raise serializers.ValidationError({
                "module": (
                    f"ContentType not found for "
                    f"{app_label}.{model_name}."
                )
            })

        # ----------------------------------------------------
        # Get related model
        # ----------------------------------------------------

        model_class = content_type.model_class()

        if model_class is None:
            raise serializers.ValidationError({
                "module": "Related model could not be found."
            })

        # ----------------------------------------------------
        # Check related object
        # ----------------------------------------------------

        if not model_class.objects.filter(id=module_id).exists():
            raise serializers.ValidationError({
                "module_id": (
                    f"{module.title()} with ID "
                    f"{module_id} does not exist."
                )
            })

        # ----------------------------------------------------
        # Save internal values
        # ----------------------------------------------------

        attrs["_sender"] = sender
        attrs["_content_type"] = content_type
        attrs["_object_id"] = module_id
        attrs["module"] = module

        return attrs

    # ========================================================
    # CREATE
    # ========================================================

    @transaction.atomic
    def create(self, validated_data):

        sender = validated_data.pop("_sender")
        content_type = validated_data.pop("_content_type")
        object_id = validated_data.pop("_object_id")

        # Remove input-only fields
        validated_data.pop("sender_id", None)
        validated_data.pop("module", None)
        validated_data.pop("module_id", None)

        # ----------------------------------------------------
        # Create central Activity
        # ----------------------------------------------------

        activity = Activity.objects.create(
            activity_type="meeting",
            created_by=sender,
            content_type=content_type,
            object_id=object_id,
        )

        # ----------------------------------------------------
        # Create Meeting
        # ----------------------------------------------------

        meeting = Meeting.objects.create(
            activity=activity,
            owner=sender,
            **validated_data
        )

        return meeting

    # ========================================================
    # UPDATE
    # ========================================================

    @transaction.atomic
    def update(self, instance, validated_data):

        # Remove input-only fields
        validated_data.pop("sender_id", None)
        validated_data.pop("module", None)
        validated_data.pop("module_id", None)

        # Remove internal values if present
        validated_data.pop("_sender", None)
        validated_data.pop("_content_type", None)
        validated_data.pop("_object_id", None)

        # ----------------------------------------------------
        # Handle attendees separately
        # ----------------------------------------------------

        attendees = validated_data.pop(
            "attendees",
            serializers.empty
        )

        # ----------------------------------------------------
        # Update normal fields
        # ----------------------------------------------------

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        # ----------------------------------------------------
        # Update attendees
        # ----------------------------------------------------

        if attendees is not serializers.empty:
            instance.attendees.set(attendees)

        return instance


# ============================================================
# MEETING RESPONSE SERIALIZER
# ============================================================

class MeetingResponseSerializer(serializers.ModelSerializer):

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

    # ========================================================
    # CREATED BY
    # ========================================================

    def get_created_by(self, obj):

        user = obj.owner

        if not user:
            return None

        name = (
            user.get_full_name()
            if hasattr(user, "get_full_name")
            else ""
        )

        if not name:
            name = getattr(user, "email", None)

        return {
            "id": user.id,
            "name": name,
        }

    # ========================================================
    # MODULE
    # ========================================================

    def get_module(self, obj):

        if not obj.activity:
            return None

        if not obj.activity.content_type:
            return None

        return obj.activity.content_type.model

    # ========================================================
    # RELATED OBJECT
    # ========================================================

    def get_lead(self, obj):

        if not obj.activity:
            return None

        content_type = obj.activity.content_type

        if not content_type:
            return None

        object_id = obj.activity.object_id

        if not object_id:
            return None

        model_name = content_type.model

        # ----------------------------------------------------
        # Get related object
        # ----------------------------------------------------

        try:
            related_object = content_type.get_object_for_this_type(
                id=object_id
            )
        except Exception:
            return None

        if not related_object:
            return None

        # ====================================================
        # LEAD
        # ====================================================

        if model_name == "lead":

            first_name = getattr(
                related_object,
                "first_name",
                ""
            )

            last_name = getattr(
                related_object,
                "last_name",
                ""
            )

            full_name = f"{first_name} {last_name}".strip()

            if not full_name:
                user = getattr(
                    related_object,
                    "user",
                    None
                )

                if user:

                    full_name = (
                        user.get_full_name()
                        if hasattr(
                            user,
                            "get_full_name"
                        )
                        else ""
                    )

                    if not full_name:
                        full_name = getattr(
                            user,
                            "email",
                            ""
                        )

            return {
                "id": related_object.id,
                "name": full_name,
            }

        # ====================================================
        # DEAL
        # ====================================================

        if model_name == "deal":

            associated_lead = getattr(
                related_object,
                "associated_lead",
                None
            )

            if associated_lead:

                first_name = getattr(
                    associated_lead,
                    "first_name",
                    ""
                )

                last_name = getattr(
                    associated_lead,
                    "last_name",
                    ""
                )

                lead_name = (
                    f"{first_name} {last_name}"
                ).strip()

                if not lead_name:

                    user = getattr(
                        associated_lead,
                        "user",
                        None
                    )

                    if user:

                        lead_name = (
                            user.get_full_name()
                            if hasattr(
                                user,
                                "get_full_name"
                            )
                            else ""
                        )

                        if not lead_name:
                            lead_name = getattr(
                                user,
                                "email",
                                ""
                            )

                return {
                    "id": associated_lead.id,
                    "name": lead_name,
                }

            # If deal has no associated lead,
            # return the deal itself.

            return {
                "id": related_object.id,
                "name": getattr(
                    related_object,
                    "deal_name",
                    getattr(
                        related_object,
                        "name",
                        str(related_object)
                    )
                ),
            }

        # ====================================================
        # COMPANY
        # ====================================================

        if model_name == "company":

            return {
                "id": related_object.id,
                "name": getattr(
                    related_object,
                    "company_name",
                    getattr(
                        related_object,
                        "name",
                        str(related_object)
                    )
                ),
            }

        # ====================================================
        # TICKET
        # ====================================================

        if model_name == "ticket":

            return {
                "id": related_object.id,
                "name": getattr(
                    related_object,
                    "ticket_name",
                    getattr(
                        related_object,
                        "name",
                        str(related_object)
                    )
                ),
            }

        # ====================================================
        # FALLBACK
        # ====================================================

        return {
            "id": related_object.id,
            "name": str(related_object),
        }

    # ========================================================
    # ATTENDEES
    # ========================================================

    def get_attendees(self, obj):

        attendees = obj.attendees.all()

        result = []

        for user in attendees:

            name = (
                user.get_full_name()
                if hasattr(user, "get_full_name")
                else ""
            )

            if not name:
                name = getattr(
                    user,
                    "email",
                    ""
                )

            result.append({
                "id": user.id,
                "name": name,
            })

        return result
