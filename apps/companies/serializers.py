
from rest_framework import serializers

from .models import Company


# =========================================================
# COMPANY CREATE SERIALIZER
# =========================================================

class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company

        fields = [
            "domain_name",
            "company_name",
            "company_owner",
            "industry",
            "type",
            "city",
            "country_region",
            "no_of_employees",
            "annual_revenue",
            "phone_number",
            "email",
        ]


# =========================================================
# COMPANY LIST / DETAIL SERIALIZER
# =========================================================

class CompanyListSerializer(serializers.ModelSerializer):

    company_owner_name = serializers.SerializerMethodField()

    def get_company_owner_name(self, obj):
        if not obj.company_owner:
            return ""

        full_name = (
            f"{obj.company_owner.first_name or ''} "
            f"{obj.company_owner.last_name or ''}"
        ).strip()

        return full_name or obj.company_owner.email

    class Meta:
        model = Company

        fields = [
            "id",
            "domain_name",
            "company_name",
            "company_owner",
            "company_owner_name",
            "industry",
            "type",
            "city",
            "country_region",
            "no_of_employees",
            "annual_revenue",
            "phone_number",
            "email",
            "created_date",
            "updated_at",
        ]


# =========================================================
# COMPANY UPDATE SERIALIZER
# =========================================================

class UpdateCompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company

        fields = [
            "domain_name",
            "company_name",
            "company_owner",
            "industry",
            "type",
            "city",
            "country_region",
            "no_of_employees",
            "annual_revenue",
            "phone_number",
            "email",
        ]