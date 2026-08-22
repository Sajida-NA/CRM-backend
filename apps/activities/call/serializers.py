from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

from .models import Call
from apps.activities.activity.models import Activity


User = get_user_model()


class CallSerializer(serializers.ModelSerializer):

    # =================================================
    # INPUT ONLY
    # =================================================

    module = serializers.CharField(
        write_only=True,
        required=True
    )

    module_id = serializers.IntegerField(
        write_only=True,
        required=True
    )

    sender_id = serializers.IntegerField(
        write_only=True,
        required=True
    )

    # =================================================
    # OUTPUT ONLY
    # =================================================

    created_by = serializers.SerializerMethodField(
        read_only=True
    )

    # =================================================
    # META
    # =================================================

    class Meta:

        model = Call

        fields = [

            # -----------------------------------------
            # Call ID
            # -----------------------------------------

            "id",

            # -----------------------------------------
            # Created By
            # -----------------------------------------

            "created_by",

            # -----------------------------------------
            # Input Fields
            # -----------------------------------------

            "module",
            "module_id",
            "sender_id",

            # -----------------------------------------
            # Call Details
            # -----------------------------------------

            "call_outcome",
            "date",
            "time",
            "note",

            # -----------------------------------------
            # Timestamps
            # -----------------------------------------

            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_by",
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
        # SAVE NORMALIZED MODULE
        # =================================================

        attrs["module"] = module

        return attrs

    # =================================================
    # CREATE
    # =================================================

    def create(self, validated_data):

        # =================================================
        # GET INPUT VALUES
        # =================================================

        module = validated_data.pop(
            "module"
        )

        module_id = validated_data.pop(
            "module_id"
        )

        sender_id = validated_data.pop(
            "sender_id"
        )

        # =================================================
        # GET CONTENT TYPE
        # =================================================

        content_type = ContentType.objects.get(
            model=module
        )

        # =================================================
        # CREATE BASE ACTIVITY
        # =================================================

        activity = Activity.objects.create(

            activity_type="call",

            created_by_id=sender_id,

            content_type=content_type,

            object_id=module_id
        )

        # =================================================
        # CREATE CALL
        # =================================================

        call = Call.objects.create(

            activity=activity,

            connected_content_type=content_type,

            connected_object_id=module_id,

            **validated_data
        )

        return call

    # =================================================
    # UPDATE
    # =================================================

    def update(
        self,
        instance,
        validated_data
    ):

        # =================================================
        # THESE CANNOT BE CHANGED
        # =================================================

        validated_data.pop(
            "module",
            None
        )

        validated_data.pop(
            "module_id",
            None
        )

        validated_data.pop(
            "sender_id",
            None
        )

        # =================================================
        # UPDATE CALL DETAILS
        # =================================================

        fields = [
            "call_outcome",
            "date",
            "time",
            "note",
        ]

        for field in fields:

            if field in validated_data:

                setattr(
                    instance,
                    field,
                    validated_data[field]
                )

        instance.save()

        return instance

    # =================================================
    # CREATED BY
    # =================================================

    def get_created_by(self, obj):

        # =================================================
        # CHECK ACTIVITY
        # =================================================

        if not obj.activity:

            return None

        # =================================================
        # GET USER
        # =================================================

        user = obj.activity.created_by

        if not user:

            return None

        # =================================================
        # GET USER NAME
        # =================================================

        full_name = user.get_full_name()

        if full_name:

            name = full_name

        else:

            name = user.email

        # =================================================
        # RETURN USER DETAILS
        # =================================================

        return {
            "id": user.id,
            "name": name
        }

    # =================================================
    # GET OBJECT NAME
    # =================================================

    def get_object_name(
        self,
        connected_object
    ):

        # =================================================
        # LEAD
        # =================================================

        if hasattr(
            connected_object,
            "first_name"
        ):

            first_name = (
                getattr(
                    connected_object,
                    "first_name",
                    ""
                )
                or ""
            )

            last_name = (
                getattr(
                    connected_object,
                    "last_name",
                    ""
                )
                or ""
            )

            full_name = (
                f"{first_name} {last_name}"
            ).strip()

            if full_name:

                return full_name

        # =================================================
        # DEAL
        # =================================================

        if hasattr(
            connected_object,
            "deal_name"
        ):

            return connected_object.deal_name

        # =================================================
        # COMPANY
        # =================================================

        if hasattr(
            connected_object,
            "company_name"
        ):

            return connected_object.company_name

        # =================================================
        # TICKET
        # =================================================

        if hasattr(
            connected_object,
            "title"
        ):

            return connected_object.title

        # =================================================
        # GENERIC NAME FIELD
        # =================================================

        if hasattr(
            connected_object,
            "name"
        ):

            return connected_object.name

        # =================================================
        # FALLBACK
        # =================================================

        return str(
            connected_object
        )

    # =================================================
    # FINAL RESPONSE
    # =================================================

    def to_representation(
        self,
        instance
    ):

        # =================================================
        # GET NORMAL SERIALIZER DATA
        # =================================================

        data = super().to_representation(
            instance
        )

        # =================================================
        # GET CONNECTED OBJECT
        # =================================================

        connected_object = instance.connected

        # =================================================
        # GET MODULE
        # =================================================

        module = (
            instance
            .connected_content_type
            .model
            .lower()
        )

        # =================================================
        # ADD MODULE
        # =================================================

        data["module"] = module

        # =================================================
        # ADD MODULE OBJECT
        # =================================================

        if connected_object:

            object_name = self.get_object_name(
                connected_object
            )

            data[module] = {
                "id": instance.connected_object_id,
                "name": object_name
            }

        else:

            data[module] = None

        # =================================================
        # REMOVE INPUT-ONLY FIELDS
        # =================================================

        data.pop(
            "module_id",
            None
        )

        data.pop(
            "sender_id",
            None
        )

        # =================================================
        # ARRANGE RESPONSE ORDER
        # =================================================

        response = {}

        response["id"] = data.pop(
            "id"
        )

        response["created_by"] = data.pop(
            "created_by"
        )

        response["module"] = data.pop(
            "module"
        )

        # =================================================
        # ADD DYNAMIC MODULE
        # =================================================

        response[module] = data.pop(
            module
        )

        # =================================================
        # ADD REST OF DETAILS
        # =================================================

        response.update(data)

        return response