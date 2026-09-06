


from django.db import transaction
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from apps.activities.activity.models import Activity
from .models import Call


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

            # Call fields
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

    def validate(self, attrs):
        module = attrs.get("module", "").strip().lower()
        module_id = attrs.get("module_id")
        sender_id = attrs.get("sender_id")

        allowed_modules = [
            "lead",
            "company",
            "deal",
            "ticket",
        ]

        if module not in allowed_modules:
            raise serializers.ValidationError({
                "module": (
                    "Invalid module. "
                    "Allowed values: lead, company, deal, ticket."
                )
            })

        if not module_id:
            raise serializers.ValidationError({
                "module_id": "Module ID is required."
            })

        if not sender_id:
            raise serializers.ValidationError({
                "sender_id": "Sender ID is required."
            })

        try:
            content_type = ContentType.objects.get(model=module)
        except ContentType.DoesNotExist:
            raise serializers.ValidationError({
                "module": f"Content type for '{module}' does not exist."
            })

        model_class = content_type.model_class()

        if not model_class:
            raise serializers.ValidationError({
                "module": f"Model for '{module}' could not be found."
            })

        if not model_class.objects.filter(id=module_id).exists():
            raise serializers.ValidationError({
                "module_id": (
                    f"{module.title()} with ID {module_id} does not exist."
                )
            })

        # Check sender
        from django.contrib.auth import get_user_model

        User = get_user_model()

        if not User.objects.filter(id=sender_id).exists():
            raise serializers.ValidationError({
                "sender_id": "User does not exist."
            })

        duration = attrs.get("duration")

        if duration is not None and duration <= 0:
            raise serializers.ValidationError({
                "duration": "Duration must be greater than 0."
            })

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