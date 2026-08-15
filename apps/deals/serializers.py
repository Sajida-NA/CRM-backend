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
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "deal_owner",
            "created_at",
            "updated_at",
        ]

    def validate_associated_lead(self, lead):

        if not lead.contact_owner:
            raise serializers.ValidationError(
                "This lead does not have a contact owner."
            )

        return lead

    def create(self, validated_data):

        # Get selected Lead
        lead = validated_data["associated_lead"]

        # Automatically get Contact Owner
        validated_data["deal_owner"] = lead.contact_owner

        # Create Deal
        deal = Deal.objects.create(
            **validated_data
        )

        # Update Lead status
        lead.lead_status = deal.deal_stage
        lead.save(
            update_fields=["lead_status"]
        )

        return deal

    def update(self, instance, validated_data):

        # Get associated Lead
        lead = validated_data.get(
            "associated_lead",
            instance.associated_lead
        )

        if not lead.contact_owner:
            raise serializers.ValidationError(
                "This lead does not have a contact owner."
            )

        # Automatically update Deal Owner
        validated_data["deal_owner"] = lead.contact_owner

        # Update Deal
        instance = super().update(
            instance,
            validated_data
        )

        # Update Lead status
        lead.lead_status = instance.deal_stage
        lead.save(
            update_fields=["lead_status"]
        )

        return instance


class DealListSerializer(serializers.ModelSerializer):

    lead_name = serializers.SerializerMethodField()

    # Same field name: deal_owner
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
            "priority",
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