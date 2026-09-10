


from django.db import transaction
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from apps.activities.activity.models import Activity
from .models import Call
from django.contrib.auth import get_user_model


class CallSerializer(serializers.ModelSerializer):
    module = serializers.CharField(write_only=True)
    module_id = serializers.IntegerField(write_only=True)
    sender_id = serializers.IntegerField(write_only=True)

    created_by = serializers.SerializerMethodField(read_only=True)

    # This will contain the connected record information
    connected = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Call
        fields = [
            "id",
            "created_by",

            # Write fields
            "module",
            "module_id",
            "sender_id",

            # -----------------------------------------
            # Call Details
            # -----------------------------------------

            "call_outcome",
            "duration",
            "date",
            "time",
            "note",

            # Connected record
            "connected",

            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_by",
            "connected",
            "created_at",
            "updated_at",
        ]

    # =================================================
    # VALIDATION
    # =================================================

    def validate(self, attrs):

        module = attrs.get("module")

        module_id = attrs.get(
            "module_id"
        )

        sender_id = attrs.get(
            "sender_id"
        )

        # =================================================
        # CHECK MODULE
        # =================================================

        if not module:

            raise serializers.ValidationError({
                "module": "Module is required."
            })

        # =================================================
        # CHECK MODULE ID
        # =================================================

        if module_id is None:

            raise serializers.ValidationError({
                "module_id": "Module ID is required."
            })

        # =================================================
        # CHECK SENDER ID
        # =================================================

        if sender_id is None:

            raise serializers.ValidationError({
                "sender_id": "Sender ID is required."
            })

        # =================================================
        # NORMALIZE MODULE
        # =================================================

        module = module.lower().strip()

        # =================================================
        # ALLOWED MODULES
        # =================================================

        allowed_modules = [
            "lead",
            "deal",
            "company",
            "ticket",
        ]

        if module not in allowed_modules:

            raise serializers.ValidationError({
                "module": (
                    "Invalid module. "
                    "Allowed modules are: "
                    "lead, deal, company, ticket."
                )
            })

        # =================================================
        # GET CONTENT TYPE
        # =================================================

        try:

            content_type = ContentType.objects.get(
                model=module
            )

        except ContentType.DoesNotExist:

            raise serializers.ValidationError({
                "module": (
                    f"Model '{module}' "
                    "does not exist."
                )
            })

        # =================================================
        # GET MODEL CLASS
        # =================================================

        model_class = content_type.model_class()

        if model_class is None:

            raise serializers.ValidationError({
                "module": (
                    f"Could not find model "
                    f"for '{module}'."
                )
            })

        # =================================================
        # CHECK CRM OBJECT EXISTS
        # =================================================

        if not model_class.objects.filter(
            pk=module_id
        ).exists():

            raise serializers.ValidationError({
                "module_id": (
                    f"{module} with id "
                    f"{module_id} does not exist."
                )
            })

        # =================================================
        # CHECK USER EXISTS
        # =================================================
        
        User = get_user_model()

        if not User.objects.filter(
            pk=sender_id
        ).exists():

            raise serializers.ValidationError({
                "sender_id": (
                    f"User with id "
                    f"{sender_id} does not exist."
                )
            })

        # =================================================
        # VALIDATE DURATION
        # =================================================

        duration = attrs.get("duration")

        if duration is not None:

            if duration <= 0:

                raise serializers.ValidationError({
                    "duration": (
                        "Duration must be greater than 0."
                    )
                })

        # =================================================
        # SAVE NORMALIZED MODULE
        # =================================================

        attrs["module"] = module

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        module = validated_data.pop("module")
        module_id = validated_data.pop("module_id")
        sender_id = validated_data.pop("sender_id")

        content_type = ContentType.objects.get(model=module)

        activity = Activity.objects.create(
            activity_type="call",
            created_by_id=sender_id,
            content_type=content_type,
            object_id=module_id,
        )

        call = Call.objects.create(
            activity=activity,
            connected_content_type=content_type,
            connected_object_id=module_id,
            **validated_data,
        )

        return call

    def update(self, instance, validated_data):
        # module/module_id/sender_id cannot be changed
        validated_data.pop("module", None)
        validated_data.pop("module_id", None)
        validated_data.pop("sender_id", None)

        return super().update(instance, validated_data)

    def get_created_by(self, obj):
        user = obj.activity.created_by

        if not user:
            return None

        return {
            "id": user.id,
            "name": (
                user.get_full_name()
                or getattr(user, "username", None)
                or user.email
            ),
        }

    def get_object_name(self, obj, module):
        """
        Return the proper display name for
        Lead / Company / Deal / Ticket.
        """

        if module == "lead":
            first_name = getattr(obj, "first_name", "")
            last_name = getattr(obj, "last_name", "")

            name = f"{first_name} {last_name}".strip()

            if name:
                return name

            return getattr(obj, "email", str(obj))

        if module == "company":
            return (
                getattr(obj, "company_name", None)
                or getattr(obj, "name", None)
                or str(obj)
            )

        if module == "deal":
            return (
                getattr(obj, "deal_name", None)
                or getattr(obj, "name", None)
                or str(obj)
            )

        if module == "ticket":
            return (
                getattr(obj, "title", None)
                or getattr(obj, "ticket_name", None)
                or getattr(obj, "name", None)
                or str(obj)
            )

        return str(obj)

    def get_connected(self, obj):
        """
        Return the connected Lead / Company / Deal / Ticket.
        """

        if not obj.connected:
            return None

        content_type = obj.connected_content_type
        connected_object = obj.connected

        module = content_type.model.lower()

        return {
            "id": obj.connected_object_id,
            "name": self.get_object_name(
                connected_object,
                module
            ),
            "module": module,
        }
