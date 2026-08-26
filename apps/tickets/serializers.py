from rest_framework import serializers

from apps.accounts.models import User
from .models import Ticket


# =====================================================
# CREATE TICKET SERIALIZER
# =====================================================

class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = (
            "id",
            "ticket_name",
            "description",
            "ticket_status",
            "source",
            "priority",
            "ticket_owner",
            "associated_deal",
            "created_date",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "created_date",
            "updated_at",
        )


# =====================================================
# TICKET LIST SERIALIZER
# =====================================================

class TicketListSerializer(serializers.ModelSerializer):

    # Display deal name instead of deal ID
    deal_name = serializers.CharField(
        source="associated_deal.deal_name",
        read_only=True
    )

    # Display owner's name instead of owner ID
    ticket_owner = serializers.SerializerMethodField()

    class Meta:
        model = Ticket

        fields = (
            "id",
            "ticket_name",
            "deal_name",
            "ticket_status",
            "priority",
            "source",
            "ticket_owner",
            "created_date",
        )

    def get_ticket_owner(self, obj):
        user = obj.ticket_owner

        # If your User model has first_name and last_name
        full_name = f"{user.first_name} {user.last_name}".strip()

        # Return full name, otherwise return email
        if full_name:
            return full_name

        return user.email


# =====================================================
# UPDATE TICKET SERIALIZER
# =====================================================

class UpdateTicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket

        fields = (
            "ticket_name",
            "description",
            "ticket_status",
            "source",
            "priority",
            "ticket_owner",
            "associated_deal",
        )