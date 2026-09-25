
# from rest_framework import serializers

# from .models import Deal


# # =========================================================
# # DEAL CREATE / UPDATE SERIALIZER
# # =========================================================

# class DealCreateSerializer(serializers.ModelSerializer):

#     lead_name = serializers.SerializerMethodField()
#     lead_phone = serializers.SerializerMethodField()

#     # Read-only owner details.
#     #
#     # IMPORTANT:
#     # deal_owners itself remains writable because the
#     # Deal Create/Edit page needs to send owner IDs.
#     deal_owner_details = serializers.SerializerMethodField()

#     class Meta:
#         model = Deal

#         fields = [
#             "id",
#             "deal_name",
#             "deal_stage",
#             "associated_lead",
#             "lead_name",
#             "lead_phone",
#             "amount",
#             "deal_owners",
#             "deal_owner_details",
#             "close_date",
#             "priority",
#             "created_date",
#             "updated_at",
#         ]

#         read_only_fields = [
#             "id",
#             "created_date",
#             "updated_at",
#             "lead_name",
#             "lead_phone",
#             "deal_owner_details",
#         ]

#     # ---------------------------------------------------------
#     # LEAD NAME
#     # ---------------------------------------------------------

#     def get_lead_name(self, obj):

#         if not obj.associated_lead:
#             return ""

#         return (
#             f"{obj.associated_lead.first_name} "
#             f"{obj.associated_lead.last_name}"
#         ).strip()

#     # ---------------------------------------------------------
#     # LEAD PHONE
#     # ---------------------------------------------------------

#     def get_lead_phone(self, obj):

#         if not obj.associated_lead:
#             return ""

#         return obj.associated_lead.phone_number or ""

#     # ---------------------------------------------------------
#     # DEAL OWNER DETAILS
#     # ---------------------------------------------------------

#     def get_deal_owner_details(self, obj):

#         owners = obj.deal_owners.all()

#         return [
#             {
#                 "id": owner.id,
#                 "first_name": owner.first_name,
#                 "last_name": owner.last_name,
#                 "email": owner.email,
#             }
#             for owner in owners
#         ]

#     # ---------------------------------------------------------
#     # CREATE
#     # ---------------------------------------------------------

#     def create(self, validated_data):

#         lead = validated_data["associated_lead"]

#         # Prevent creating another Deal from an already
#         # converted Lead.
#         if lead.lead_status == "Converted":

#             raise serializers.ValidationError(
#                 {
#                     "associated_lead": (
#                         "This lead is already converted."
#                     )
#                 }
#             )

#         # Remove ManyToMany data before creating Deal.
#         deal_owners = validated_data.pop(
#             "deal_owners",
#             []
#         )

#         # Create Deal.
#         deal = Deal.objects.create(
#             **validated_data
#         )

#         # Set Deal Owners.
#         deal.deal_owners.set(
#             deal_owners
#         )

#         # Mark Lead as Converted.
#         lead.lead_status = "Converted"

#         lead.save(
#             update_fields=[
#                 "lead_status"
#             ]
#         )

#         return deal

#     # ---------------------------------------------------------
#     # UPDATE
#     # ---------------------------------------------------------

#     def update(self, instance, validated_data):

#         # Get owners if supplied.
#         #
#         # None means the frontend did not send
#         # deal_owners, so keep the existing owners.
#         deal_owners = validated_data.pop(
#             "deal_owners",
#             None
#         )

#         # Update normal Deal fields.
#         instance = super().update(
#             instance,
#             validated_data
#         )

#         # Update Deal Owners only when supplied.
#         if deal_owners is not None:

#             instance.deal_owners.set(
#                 deal_owners
#             )

#         return instance


# # =========================================================
# # DEAL LIST / DETAIL SERIALIZER
# # =========================================================

# class DealListSerializer(serializers.ModelSerializer):

#     lead_name = serializers.SerializerMethodField()
#     lead_phone = serializers.SerializerMethodField()

#     # Existing Deal owner names.
#     deal_owners = serializers.SerializerMethodField()

#     # Existing Deal owner IDs.
#     deal_owner_ids = serializers.PrimaryKeyRelatedField(
#         source="deal_owners",
#         many=True,
#         read_only=True
#     )

#     # ---------------------------------------------------------
#     # NEW
#     #
#     # Used by Create Ticket Drawer to show only the owners
#     # of the selected Closed Won Deal.
#     # ---------------------------------------------------------

#     deal_owner_details = serializers.SerializerMethodField()

#     class Meta:
#         model = Deal

#         fields = [
#             "id",
#             "deal_name",
#             "associated_lead",
#             "lead_name",
#             "lead_phone",
#             "deal_stage",
#             "close_date",
#             "deal_owners",
#             "deal_owner_ids",
#             "deal_owner_details",
#             "amount",
#             "priority",
#             "created_date",
#         ]

#     # ---------------------------------------------------------
#     # LEAD NAME
#     # ---------------------------------------------------------

#     def get_lead_name(self, obj):

#         if not obj.associated_lead:
#             return ""

#         return (
#             f"{obj.associated_lead.first_name} "
#             f"{obj.associated_lead.last_name}"
#         ).strip()

#     # ---------------------------------------------------------
#     # LEAD PHONE
#     # ---------------------------------------------------------

#     def get_lead_phone(self, obj):

#         if not obj.associated_lead:
#             return ""

#         return obj.associated_lead.phone_number or ""

#     # ---------------------------------------------------------
#     # DEAL OWNER NAMES
#     # ---------------------------------------------------------

#     def get_deal_owners(self, obj):

#         owners = obj.deal_owners.all()

#         return [
#             (
#                 f"{owner.first_name} "
#                 f"{owner.last_name}"
#             ).strip()
#             for owner in owners
#         ]

#     # ---------------------------------------------------------
#     # DEAL OWNER DETAILS
#     # ---------------------------------------------------------

#     def get_deal_owner_details(self, obj):

#         owners = obj.deal_owners.all()

#         return [
#             {
#                 "id": owner.id,
#                 "first_name": owner.first_name,
#                 "last_name": owner.last_name,
#                 "email": owner.email,
#             }
#             for owner in owners
#         ]

from rest_framework import serializers

from .models import Deal


# =========================================================
# DEAL CREATE / UPDATE SERIALIZER
# =========================================================

class DealCreateSerializer(serializers.ModelSerializer):

    lead_name = serializers.SerializerMethodField()
    lead_phone = serializers.SerializerMethodField()

    # All Deal Owner details
    #
    # This remains read-only.
    # deal_owners itself is still writable.
    deal_owner_details = serializers.SerializerMethodField()

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
            "deal_owners",
            "deal_owner_details",
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
            "deal_owner_details",
        ]

    # ---------------------------------------------------------
    # LEAD NAME
    # ---------------------------------------------------------

    def get_lead_name(self, obj):
        if not obj.associated_lead:
            return ""

        return (
            f"{obj.associated_lead.first_name} "
            f"{obj.associated_lead.last_name}"
        ).strip()

    # ---------------------------------------------------------
    # LEAD PHONE
    # ---------------------------------------------------------

    def get_lead_phone(self, obj):
        if not obj.associated_lead:
            return ""

        return obj.associated_lead.phone_number or ""

    # ---------------------------------------------------------
    # DEAL OWNER DETAILS
    # ---------------------------------------------------------

    def get_deal_owner_details(self, obj):
        owners = obj.deal_owners.all()

        return [
            {
                "id": owner.id,
                "first_name": owner.first_name,
                "last_name": owner.last_name,
                "email": owner.email,
            }
            for owner in owners
        ]

    # ---------------------------------------------------------
    # CREATE
    # ---------------------------------------------------------

    def create(self, validated_data):

        lead = validated_data["associated_lead"]

        # Prevent creating another Deal from an
        # already converted Lead.
        if lead.lead_status == "Converted":
            raise serializers.ValidationError(
                {
                    "associated_lead": (
                        "This lead is already converted."
                    )
                }
            )

        # Remove M2M data before creating Deal.
        deal_owners = validated_data.pop(
            "deal_owners",
            []
        )

        # Create Deal.
        deal = Deal.objects.create(
            **validated_data
        )

        # Set all Deal Owners.
        deal.deal_owners.set(
            deal_owners
        )

        # Mark Lead as Converted.
        lead.lead_status = "Converted"

        lead.save(
            update_fields=[
                "lead_status"
            ]
        )

        return deal

    # ---------------------------------------------------------
    # UPDATE
    # ---------------------------------------------------------

    def update(self, instance, validated_data):

        # If deal_owners is not supplied,
        # existing owners are preserved.
        deal_owners = validated_data.pop(
            "deal_owners",
            None
        )

        # Update normal Deal fields.
        instance = super().update(
            instance,
            validated_data
        )

        # Update owners only when supplied.
        if deal_owners is not None:
            instance.deal_owners.set(
                deal_owners
            )

        return instance


# =========================================================
# DEAL LIST / DETAIL SERIALIZER
# =========================================================

class DealListSerializer(serializers.ModelSerializer):

    lead_name = serializers.SerializerMethodField()
    lead_phone = serializers.SerializerMethodField()

    # Deal Owner names
    deal_owners = serializers.SerializerMethodField()

    # Deal Owner IDs
    deal_owner_ids = serializers.PrimaryKeyRelatedField(
        source="deal_owners",
        many=True,
        read_only=True
    )

    # Full Deal Owner details
    #
    # IMPORTANT:
    # This returns ALL owners of the Deal.
    deal_owner_details = serializers.SerializerMethodField()

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
            "deal_owners",
            "deal_owner_ids",
            "deal_owner_details",
            "amount",
            "priority",
            "created_date",
        ]

    # ---------------------------------------------------------
    # LEAD NAME
    # ---------------------------------------------------------

    def get_lead_name(self, obj):
        if not obj.associated_lead:
            return ""

        return (
            f"{obj.associated_lead.first_name} "
            f"{obj.associated_lead.last_name}"
        ).strip()

    # ---------------------------------------------------------
    # LEAD PHONE
    # ---------------------------------------------------------

    def get_lead_phone(self, obj):
        if not obj.associated_lead:
            return ""

        return obj.associated_lead.phone_number or ""

    # ---------------------------------------------------------
    # DEAL OWNER NAMES
    # ---------------------------------------------------------

    def get_deal_owners(self, obj):

        owners = obj.deal_owners.all()

        return [
            (
                f"{owner.first_name} "
                f"{owner.last_name}"
            ).strip()
            for owner in owners
        ]

    # ---------------------------------------------------------
    # DEAL OWNER DETAILS
    # ---------------------------------------------------------

    def get_deal_owner_details(self, obj):

        owners = obj.deal_owners.all()

        return [
            {
                "id": owner.id,
                "first_name": owner.first_name,
                "last_name": owner.last_name,
                "email": owner.email,
            }
            for owner in owners
        ]