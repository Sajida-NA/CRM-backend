from rest_framework import serializers

from .models import Deal


class DealCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Deal

        fields = [
            "id",
            "deal_name",
            "deal_stage",
            "associated_lead",
            "amount",
            "deal_owner",
            "close_date",
            "priority",
            "created_date",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_date",
            "updated_at",
        ]

    def create(self, validated_data):

        # Get the selected Lead
        lead = validated_data["associated_lead"]

        # Create Deal
        deal = Deal.objects.create(
            **validated_data
        )

        # Update Lead status based on Deal stage
        lead.lead_status = deal.deal_stage

        lead.save(
            update_fields=["lead_status"]
        )

        return deal

    def update(self, instance, validated_data):

        # Update Deal
        instance = super().update(
            instance,
            validated_data
        )

        # Get the associated Lead
        lead = instance.associated_lead

        # Update Lead status based on Deal stage
        lead.lead_status = instance.deal_stage

        lead.save(
            update_fields=["lead_status"]
        )

        return instance


class DealListSerializer(serializers.ModelSerializer):

    lead_name = serializers.SerializerMethodField()

    # Response will show owner's name instead of ID
    deal_owner = serializers.SerializerMethodField()

    class Meta:
        model = Deal

        fields = [
            "id",
            "deal_name",
            "lead_name",
            "deal_stage",
            "close_date",
            "deal_owner",
            "amount",
        ]

    def get_lead_name(self, obj):

        return (
            f"{obj.associated_lead.first_name} "
            f"{obj.associated_lead.last_name}"
        ).strip()

    def get_deal_owner(self, obj):

        return (
            f"{obj.deal_owner.first_name} "
            f"{obj.deal_owner.last_name}"
        ).strip()