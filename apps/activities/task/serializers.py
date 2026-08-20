from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from rest_framework import serializers

from .models import Task
from apps.activities.activity.models import Activity


class TaskSerializer(serializers.ModelSerializer):

    # --------------------------------
    # INPUT FIELDS
    # --------------------------------

    module = serializers.CharField(
        write_only=True,
        required=False
    )

    module_id = serializers.IntegerField(
        write_only=True,
        required=False
    )

    # --------------------------------
    # RESPONSE FIELDS
    # --------------------------------

    lead_name = serializers.SerializerMethodField()

    assigned_to_name = serializers.SerializerMethodField()

    class Meta:
        model = Task

        fields = [
            "id",

            # CRM object - input only
            "module",
            "module_id",

            # Display only
            "lead_name",

            # Task details
            "task_name",
            "due_date",
            "time",
            "task_type",
            "priority",
            "note",

            # Assigned user
            "assigned_to",
            "assigned_to_name",

            # Timestamps
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "lead_name",
            "assigned_to_name",
            "created_at",
            "updated_at",
        ]

        extra_kwargs = {
            "assigned_to": {
                "write_only": True
            }
        }

    # ========================================
    # CRM OBJECT NAME
    # ========================================

    def get_lead_name(self, obj):

        related_object = obj.related_object

        if not related_object:
            return None

        # Lead
        if obj.content_type.model == "lead":

            return (
                f"{related_object.first_name} "
                f"{related_object.last_name}"
            ).strip()

        # Deal
        if obj.content_type.model == "deal":

            lead = getattr(
                related_object,
                "associated_lead",
                None
            )

            if lead:
                return (
                    f"{lead.first_name} "
                    f"{lead.last_name}"
                ).strip()

        # Company
        if obj.content_type.model == "company":

            return getattr(
                related_object,
                "name",
                None
            )

        # Ticket
        if obj.content_type.model == "ticket":

            return getattr(
                related_object,
                "name",
                None
            )

        return None

    # ========================================
    # ASSIGNED USER NAME
    # ========================================

    def get_assigned_to_name(self, obj):

        if not obj.assigned_to:
            return None

        return (
            obj.assigned_to.get_full_name()
            or obj.assigned_to.email
        )

    # ========================================
    # VALIDATE MODULE
    # ========================================

    def validate(self, attrs):

        module = attrs.pop("module", None)
        module_id = attrs.pop("module_id", None)

        # For PATCH/UPDATE
        if module is None and module_id is None:
            return attrs

        if module is None or module_id is None:

            raise serializers.ValidationError({
                "module": "Both module and module_id are required."
            })

        module = module.lower()

        MODULE_MAP = {
            "lead": ("leads", "lead"),
            "deal": ("deals", "deal"),
            "company": ("companies", "company"),
            "ticket": ("tickets", "ticket"),
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

        attrs["content_type"] = content_type
        attrs["object_id"] = module_id

        return attrs

    # ========================================
    # CREATE TASK + ACTIVITY
    # ========================================

    @transaction.atomic
    def create(self, validated_data):

        request = self.context["request"]

        content_type = validated_data["content_type"]
        object_id = validated_data["object_id"]

        activity = Activity.objects.create(
            activity_type="task",
            created_by=request.user,
            content_type=content_type,
            object_id=object_id
        )

        task = Task.objects.create(
            activity=activity,
            **validated_data
        )

        return task

    # ========================================
    # UPDATE TASK
    # ========================================

    @transaction.atomic
    def update(self, instance, validated_data):

        if "content_type" in validated_data:

            instance.content_type = validated_data.pop(
                "content_type"
            )

        if "object_id" in validated_data:

            instance.object_id = validated_data.pop(
                "object_id"
            )

        for attr, value in validated_data.items():

            setattr(
                instance,
                attr,
                value
            )

        instance.save()

        # Keep Activity connected
        # to the same CRM object

        if hasattr(instance, "activity"):

            instance.activity.content_type = (
                instance.content_type
            )

            instance.activity.object_id = (
                instance.object_id
            )

            instance.activity.save()

        return instance