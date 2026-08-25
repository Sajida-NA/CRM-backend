from rest_framework import serializers

from apps.accounts.models import User
from .models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Ticket
        fields = "__all__"


class TicketListSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Ticket
        fields = "__all__"


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
