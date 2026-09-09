# from rest_framework import serializers

# from .models import Company


# # =========================================================
# # COMPANY CREATE SERIALIZER
# # =========================================================

# class CompanySerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Company

#         # Fields accepted when creating a company
#         fields = [
#             "domain_name",
#             "company_name",
#             "company_owner",
#             "industry",
#             "type",
#             "city",
#             "country_region",
#             "no_of_employees",
#             "annual_revenue",
#             "phone_number",
#             "email",
#         ]


# # =========================================================
# # COMPANY LIST / DETAIL SERIALIZER
# # =========================================================

# class CompanyListSerializer(serializers.ModelSerializer):

#     # Display the name of the user instead of the owner ID
#     company_owner = serializers.SerializerMethodField()

#     def get_company_owner(self, obj):
#         user = obj.company_owner

#         full_name = f"{user.first_name} {user.last_name}".strip()

#         # If first and last name are empty, show email
#         return full_name if full_name else user.email

#     class Meta:
#         model = Company

#         fields = [
#             "id",
#             "domain_name",
#             "company_name",
#             "company_owner",
#             "industry",
#             "type",
#             "city",
#             "country_region",
#             "no_of_employees",
#             "annual_revenue",
#             "phone_number",
#             "email",
#             "created_date",
#             "updated_at",
#         ]


# # =========================================================
# # COMPANY UPDATE SERIALIZER
# # =========================================================

# class UpdateCompanySerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Company

#         # Fields that can be updated
#         fields = [
#             "domain_name",
#             "company_name",
#             "company_owner",
#             "industry",
#             "type",
#             "city",
#             "country_region",
#             "no_of_employees",
#             "annual_revenue",
#             "phone_number",
#             "email",
#         ]


from rest_framework import serializers

from .models import Company


# =========================================================
# COMPANY CREATE SERIALIZER
# =========================================================

class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company

        # Fields accepted when creating a company
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

    # Display the name of the user instead of the owner ID
    company_owner = serializers.SerializerMethodField()

    def get_company_owner(self, obj):
        user = obj.company_owner

        full_name = f"{user.first_name} {user.last_name}".strip()

        # If first and last name are empty, show email
        return full_name if full_name else user.email

    class Meta:
        model = Company

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


# =========================================================
# COMPANY UPDATE SERIALIZER
# =========================================================

class UpdateCompanySerializer(serializers.ModelSerializer):

    class Meta:
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
