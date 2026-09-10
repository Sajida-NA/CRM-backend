from rest_framework import serializers

from .models import Deal


# ============================================================
# CREATE / UPDATE DEAL SERIALIZER
# ============================================================

class DealCreateSerializer(serializers.ModelSerializer):

    # Lead display name
    lead_name = serializers.SerializerMethodField()

    # Lead phone number
    lead_phone = serializers.SerializerMethodField()

    class Meta:
        model = Deal

        fields = [
            "id",
            "deal_name",
            "deal_stage",
            "associated_lead",
            "lead_name",
            "lead_phone",
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
            "lead_name",
            "lead_phone",
        ]

    # ========================================================
    # LEAD NAME
    # ========================================================

    def get_lead_name(self, obj):

        if not obj.associated_lead:
            return ""

        return (
            f"{obj.associated_lead.first_name} "
            f"{obj.associated_lead.last_name}"
        ).strip()

    # ========================================================
    # LEAD PHONE
    # ========================================================

    def get_lead_phone(self, obj):

        if not obj.associated_lead:
            return ""

        return obj.associated_lead.phone_number or ""

    # ========================================================
    # CREATE DEAL + CONVERT LEAD
    # ========================================================

    def create(self, validated_data):

        # Get the selected Lead
        lead = validated_data["associated_lead"]

        # ----------------------------------------------------
        # PREVENT DOUBLE CONVERSION
        # ----------------------------------------------------

        if lead.lead_status == "Converted":

            raise serializers.ValidationError({
                "associated_lead": "This lead is already converted."
            })

        # ----------------------------------------------------
        # CREATE DEAL
        # ----------------------------------------------------

        deal = Deal.objects.create(
            **validated_data
        )

        # ----------------------------------------------------
        # CONVERT LEAD
        #
        # IMPORTANT:
        # Lead status is ALWAYS "Converted".
        #
        # It does NOT become:
        # Qualified to Buy
        # Contract Sent
        # Closed Won
        # etc.
        # ----------------------------------------------------

        lead.lead_status = "Converted"

        lead.save(
            update_fields=["lead_status"]
        )

        return deal

    # ========================================================
    # UPDATE DEAL
    # ========================================================

    def update(self, instance, validated_data):

        # ----------------------------------------------------
        # UPDATE ONLY THE DEAL
        #
        # IMPORTANT:
        # Changing Deal stage must NOT change Lead status.
        # ----------------------------------------------------

        instance = super().update(
            instance,
            validated_data
        )

        return instance


# ============================================================
# DEAL LIST SERIALIZER
# ============================================================

class DealListSerializer(serializers.ModelSerializer):

    # Lead display name
    lead_name = serializers.SerializerMethodField()

    # Lead phone number
    lead_phone = serializers.SerializerMethodField()

    # Owner display name
    deal_owner = serializers.SerializerMethodField()

    # Owner ID for Edit
    deal_owner_id = serializers.IntegerField(
        source="deal_owner.id",
        read_only=True
    )

    class Meta:
        model = Deal

        fields = [
            "id",
            "deal_name",
            "associated_lead",
            "lead_name",
            "lead_phone",
            "deal_stage",
            "close_date",
            "deal_owner",
            "deal_owner_id",
            "amount",
            "priority",
            "created_date",
        ]

    # ========================================================
    # LEAD NAME
    # ========================================================

    def get_lead_name(self, obj):

        if not obj.associated_lead:
            return ""

        return (
            f"{obj.associated_lead.first_name} "
            f"{obj.associated_lead.last_name}"
        ).strip()

    # ========================================================
    # LEAD PHONE
    # ========================================================

    def get_lead_phone(self, obj):

        if not obj.associated_lead:
            return ""

        return obj.associated_lead.phone_number or ""

    # ========================================================
    # OWNER NAME
    # ========================================================

    def get_deal_owner(self, obj):

        if not obj.deal_owner:
            return ""

        return (
            f"{obj.deal_owner.first_name} "
            f"{obj.deal_owner.last_name}"
        ).strip()
