

from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import Lead, Product


User = get_user_model()


# =========================================================
# PRODUCT SERIALIZER
# =========================================================

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product

        fields = [
            "id",
            "name",
            "description",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
        ]


# =========================================================
# LIST SERIALIZER
# Used for:
# - Leads table
# - Deal conversion
# =========================================================

class LeadListSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()

    # =====================================================
    # CONTACT OWNERS - MULTIPLE
    # =====================================================

    contact_owner_ids = serializers.SerializerMethodField()

    contact_owner_names = serializers.SerializerMethodField()

    class Meta:
        model = Lead

        fields = [
            "id",
            "name",
            "email",
            "phone_number",
            "created_date",
            "lead_status",

            # Multiple Contact Owners
            "contact_owner_ids",
            "contact_owner_names",
        ]

        read_only_fields = [
            "id",
            "created_date",
            "contact_owner_ids",
            "contact_owner_names",
        ]

    # =====================================================
    # LEAD NAME
    # =====================================================

    def get_name(self, obj):

        return (
            f"{obj.first_name} "
            f"{obj.last_name}"
        ).strip()

    # =====================================================
    # GET ALL CONTACT OWNER IDS
    # =====================================================

    def get_contact_owner_ids(self, obj):

        return list(
            obj.contact_owners
            .all()
            .order_by("id")
            .values_list(
                "id",
                flat=True,
            )
        )

    # =====================================================
    # GET ALL CONTACT OWNER NAMES
    # =====================================================

    def get_contact_owner_names(self, obj):

        return [
            (
                f"{owner.first_name} "
                f"{owner.last_name}"
            ).strip()
            for owner in (
                obj.contact_owners
                .all()
                .order_by("id")
            )
        ]


# =========================================================
# DETAIL / CREATE / UPDATE SERIALIZER
# Used for:
# - Create Lead
# - Edit Lead
# - Single Lead GET
# =========================================================

class LeadCreateSerializer(serializers.ModelSerializer):

    # =====================================================
    # PRODUCTS - MULTIPLE
    # =====================================================

    products = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        many=True,
        required=False,
    )

    # =====================================================
    # CONTACT OWNERS - MULTIPLE
    # =====================================================

    contact_owners = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        required=False,
    )

    # =====================================================
    # CONTACT OWNER IDS
    # Read-only helper field
    # =====================================================

    contact_owner_ids = serializers.SerializerMethodField()

    # =====================================================
    # CONTACT OWNER NAMES
    # Read-only helper field
    # =====================================================

    contact_owner_names = serializers.SerializerMethodField()

    class Meta:
        model = Lead

        fields = [
            "id",

            "email",

            "first_name",

            "last_name",

            "phone_number",

            "job_title",

            # Main writable field
            "contact_owners",

            # Read-only helper fields
            "contact_owner_ids",
            "contact_owner_names",

            "lead_status",

            "products",

            "company",

            "city",

            "created_date",
        ]

        read_only_fields = [
            "id",
            "created_date",
            "contact_owner_ids",
            "contact_owner_names",
        ]

    # =====================================================
    # GET ALL CONTACT OWNER IDS
    # =====================================================

    def get_contact_owner_ids(self, obj):

        return list(
            obj.contact_owners
            .all()
            .order_by("id")
            .values_list(
                "id",
                flat=True,
            )
        )

    # =====================================================
    # GET ALL CONTACT OWNER NAMES
    # =====================================================

    def get_contact_owner_names(self, obj):

        return [
            (
                f"{owner.first_name} "
                f"{owner.last_name}"
            ).strip()
            for owner in (
                obj.contact_owners
                .all()
                .order_by("id")
            )
        ]