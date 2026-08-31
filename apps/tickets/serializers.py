from rest_framework import serializers

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
# TICKET LIST / DETAIL SERIALIZER
# =====================================================

class TicketListSerializer(serializers.ModelSerializer):

    # Display deal name
    deal_name = serializers.CharField(
        source="associated_deal.deal_name",
        read_only=True
    )

    # Keep owner display name for table
    ticket_owner = serializers.SerializerMethodField()

    # IMPORTANT:
    # Send owner ID also for Edit Drawer
    ticket_owner_id = serializers.IntegerField(
        source="ticket_owner.id",
        read_only=True
    )

    # IMPORTANT:
    # Send deal ID also for Edit Drawer
    associated_deal_id = serializers.IntegerField(
        source="associated_deal.id",
        read_only=True
    )

    class Meta:
        model = Ticket

        fields = (
            "id",
            "ticket_name",
            "description",
            "deal_name",
            "associated_deal_id",
            "ticket_status",
            "priority",
            "source",
            "ticket_owner",
            "ticket_owner_id",
            "created_date",
        )

    def get_ticket_owner(self, obj):
        user = obj.ticket_owner

        if not user:
            return ""

        full_name = f"{user.first_name} {user.last_name}".strip()

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