from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from .models import Activity


class ActivitySerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(
        source="created_by.email"
    )

    entity_type = serializers.CharField(
        write_only=True,
        required=False,
    )

    entity_id = serializers.IntegerField(
        write_only=True,
        required=False,
    )

    related_object = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = [
            "id",
            "activity_type",
            "subject",
            "description",
            "created_by",
            "content_type",
            "object_id",
            "entity_type",
            "entity_id",
            "related_object",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_by",
            "content_type",
            "object_id",
            "related_object",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        entity_type = attrs.get("entity_type")
        entity_id = attrs.get("entity_id")

        if entity_type and entity_id:
            try:
                content_type = ContentType.objects.get(
                    model=entity_type.lower()
                )
            except ContentType.DoesNotExist:
                raise serializers.ValidationError(
                    {
                        "entity_type": "Invalid entity type."
                    }
                )

            try:
                content_type.get_object_for_this_type(
                    pk=entity_id
                )
            except content_type.model_class().DoesNotExist:
                raise serializers.ValidationError(
                    {
                        "entity_id": "Related object does not exist."
                    }
                )

        elif entity_type or entity_id:
            raise serializers.ValidationError(
                {
                    "entity": "entity_type and entity_id must be provided together."
                }
            )

        return attrs

    def create(self, validated_data):
        entity_type = validated_data.pop(
            "entity_type",
            None,
        )

        entity_id = validated_data.pop(
            "entity_id",
            None,
        )

        if entity_type and entity_id:
            content_type = ContentType.objects.get(
                model=entity_type.lower()
            )

            validated_data["content_type"] = content_type
            validated_data["object_id"] = entity_id

        return Activity.objects.create(
            **validated_data
        )

    def get_related_object(self, obj):
        if not obj.content_object:
            return None

        return {
            "type": obj.content_type.model,
            "id": obj.object_id,
            "name": str(obj.content_object),
        }