# from rest_framework import serializers
# 3
# from .models import Lead, Product


# class ProductSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Product
#         fields = [
#             "id",
#             "name",
#             "description",
#             "created_at",
#         ]

#         read_only_fields = [
#             "id",
#             "created_at",
#         ]


# class LeadListSerializer(serializers.ModelSerializer):

#     name = serializers.SerializerMethodField()

#     class Meta:
#         model = Lead
#         fields = [
#             "id",
#             "name",
#             "email",
#             "phone_number",
#             "created_date",
#             "lead_status",
#         ]

#         read_only_fields = [
#             "id",
#             "created_date",
#         ]

#     def get_name(self, obj):
#         return f"{obj.first_name} {obj.last_name}".strip()


# class LeadCreateSerializer(serializers.ModelSerializer):

#     products = serializers.PrimaryKeyRelatedField(
#         queryset=Product.objects.all(),
#         many=True,
#         required=False
#     )

#     class Meta:
#         model = Lead
#         fields = [
#             "id",
#             "email",
#             "first_name",
#             "last_name",
#             "phone_number",
#             "job_title",
#             "contact_owner",
#             "lead_status",
#             "products",
#             "company",
#             "city",
#             "created_date",
#         ]

#         read_only_fields = [
#             "id",
#             "created_date",
#         ]

#     def create(self, validated_data):

#         products = validated_data.pop("products", [])

#         lead = Lead.objects.create(
#             **validated_data
#         )

#         lead.products.set(products)

#         return lead

#     def update(self, instance, validated_data):

#         products = validated_data.pop("products", None)

#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)

#         instance.save()

#         if products is not None:
#             instance.products.set(products)

#         return instance


from rest_framework import serializers

from .models import Lead, Product


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
# Used only for the Leads table
# =========================================================

class LeadListSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()

    class Meta:
        model = Lead
        fields = [
            "id",
            "name",
            "email",
            "phone_number",
            "created_date",
            "lead_status",
        ]

        read_only_fields = [
            "id",
            "created_date",
        ]

    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()


# =========================================================
# DETAIL / CREATE / UPDATE SERIALIZER
# Used for Create, Edit and single Lead GET
# =========================================================

class LeadCreateSerializer(serializers.ModelSerializer):

    products = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = Lead

        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "job_title",
            "contact_owner",
            "lead_status",
            "products",
            "company",
            "city",
            "created_date",
        ]

        read_only_fields = [
            "id",
            "created_date",
        ]