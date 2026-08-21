from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType

from .models import Activity


class ActivitySerializer(serializers.ModelSerializer):

    module = serializers.SerializerMethodField()

    sender_id = serializers.SerializerMethodField()
    sender_name = serializers.SerializerMethodField()
    sender_email = serializers.SerializerMethodField()

    class Meta:
        model = Activity

        fields = [
            "id",

            # Activity
            "activity_type",

            # CRM module
            "module",
            "object_id",

            # Sender
            "sender_id",
            "sender_name",
            "sender_email",

            # Dates
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "sender_id",
            "sender_name",
            "sender_email",
            "created_at",
            "updated_at",
        ]

    # -----------------------------------
    # Module
    # -----------------------------------

    def get_module(self, obj):
        return obj.content_type.model

    # -----------------------------------
    # Sender ID
    # -----------------------------------

    def get_sender_id(self, obj):

        if not obj.created_by:
            return None

        return obj.created_by.id

    # -----------------------------------
    # Sender Name
    # -----------------------------------

    def get_sender_name(self, obj):

        user = obj.created_by

        if not user:
            return None

        return user.get_full_name() or user.email

    # -----------------------------------
    # Sender Email
    # -----------------------------------

    def get_sender_email(self, obj):

        user = obj.created_by

        if not user:
            return None

        return user.email

    # -----------------------------------
    # Validation
    # -----------------------------------

    def validate(self, attrs):

        module = self.initial_data.get("module")

        allowed_modules = [
            "lead",
            "deal",
            "company",
            "ticket",
        ]

        if not module:
            raise serializers.ValidationError({
                "module": "This field is required."
            })

        module = module.lower()

        if module not in allowed_modules:
            raise serializers.ValidationError({
                "module": (
                    f"Choose one of: {', '.join(allowed_modules)}"
                )
            })

        try:
            content_type = ContentType.objects.get(
                model=module
            )

        except ContentType.DoesNotExist:

            raise serializers.ValidationError({
                "module": f"No model found for module '{module}'."
            })

        attrs["content_type"] = content_type

        return attrs

    # -----------------------------------
    # Create
    # -----------------------------------

    def create(self, validated_data):

        request = self.context.get("request")

        if request and request.user.is_authenticated:
            validated_data["created_by"] = request.user

        return Activity.objects.create(
            **validated_data
        )