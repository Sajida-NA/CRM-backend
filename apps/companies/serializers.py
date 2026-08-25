# Import Django REST Framework serializers
from rest_framework import serializers

# Import Company model
from .models import Company


# ---------------------------------------------------------
# COMPANY CREATE SERIALIZER
# ---------------------------------------------------------

class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        # Use Company model
        model = Company

        # Fields in the exact frontend form order
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


# ---------------------------------------------------------
# COMPANY LIST / DETAIL SERIALIZER
# ---------------------------------------------------------

class CompanyListSerializer(serializers.ModelSerializer):

    # Return the owner's email
    company_owner_name = serializers.CharField(
        source="company_owner.email",
        read_only=True
    )

    class Meta:
        # Use Company model
        model = Company

        # Return fields in frontend order
        fields = [
            "id",
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
            "created_date",
            "updated_at",
        ]


# ---------------------------------------------------------
# COMPANY UPDATE SERIALIZER
# ---------------------------------------------------------

class UpdateCompanySerializer(serializers.ModelSerializer):

    class Meta:
        # Use Company model
        model = Company

        # Fields that can be updated
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