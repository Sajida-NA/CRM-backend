from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType

from .models import Activity


class ActivitySerializer(serializers.ModelSerializer):

    module = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = [
            "id",
            "activity_type",
            "module",
            "object_id",
            "created_by",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_by",
            "created_at",
            "updated_at",
        ]

    def get_module(self, obj):
        return obj.content_type.model

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
                "module": f"Choose one of: {allowed_modules}"
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

    def create(self, validated_data):
        request = self.context.get("request")

        if request and request.user.is_authenticated:
            validated_data["created_by"] = request.user

        return Activity.objects.create(**validated_data)