from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Lead


User = get_user_model()


class LeadSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        source="user.email",
        read_only=True
    )

    first_name = serializers.CharField(
        source="user.first_name",
        read_only=True
    )

    last_name = serializers.CharField(
        source="user.last_name",
        read_only=True
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
            "company_type",
            "city",
            "created_at",
            "updated_at",
        ]


class LeadListSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()

    email = serializers.EmailField(
        source="user.email",
        read_only=True
    )

    class Meta:
        model = Lead

        fields = [
            "id",
            "name",
            "email",
            "phone_number",
            "created_at",
            "lead_status",
        ]

    def get_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip()


class LeadCreateSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        write_only=True
    )

    first_name = serializers.CharField(
        write_only=True
    )

    last_name = serializers.CharField(
        write_only=True
    )

    class Meta:
        model = Lead

        fields = [
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "job_title",
            "contact_owner",
            "lead_status",
            "products",
            "company_type",
            "city",
        ]

    def validate_email(self, value):

        if User.objects.filter(email=value).exists():

            user = User.objects.get(email=value)

            if user.is_lead:
                raise serializers.ValidationError(
                    "This user is already a lead."
                )

        return value

    def create(self, validated_data):

        email = validated_data.pop("email")
        first_name = validated_data.pop("first_name")
        last_name = validated_data.pop("last_name")

        # ManyToMany field must be handled separately
        products = validated_data.pop("products", [])

        # Check if user already exists
        user = User.objects.filter(
            email=email
        ).first()

        if user:

            # Convert existing user into lead
            user.first_name = first_name
            user.last_name = last_name
            user.is_lead = True

            user.save(
                update_fields=[
                    "first_name",
                    "last_name",
                    "is_lead",
                ]
            )

        else:

            # Create a new user
            user = User.objects.create(
                email=email,
                first_name=first_name,
                last_name=last_name,
                is_lead=True,
            )

            # No password for newly-created lead
            user.set_unusable_password()
            user.save()

        # Create Lead without products
        lead = Lead.objects.create(
            user=user,
            **validated_data
        )

        # Set ManyToMany products
        lead.products.set(products)

        return lead