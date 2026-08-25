from rest_framework import serializers
from django.contrib.auth import get_user_model



User = get_user_model()



class DashboardSummarySerializer(serializers.Serializer):

    total_leads = serializers.IntegerField()

    active_deals = serializers.IntegerField()

    closed_deals = serializers.IntegerField()

    monthly_revenue = serializers.DecimalField(
        max_digits=12,
        decimal_places=2
    )


class ConversionStageSerializer(serializers.Serializer):

    count = serializers.IntegerField()

    percentage = serializers.IntegerField()


class DashboardConversionSerializer(serializers.Serializer):

    contact = ConversionStageSerializer()

    qualified_lead = ConversionStageSerializer()

    proposal_sent = ConversionStageSerializer()

    negotiation = ConversionStageSerializer()

    closed_won = ConversionStageSerializer()

    closed_lost = ConversionStageSerializer()


class SalesReportSerializer(serializers.Serializer):

    month = serializers.CharField()

    revenue = serializers.DecimalField(
        max_digits=12,
        decimal_places=2
    )


class TeamPerformanceSerializer(serializers.ModelSerializer):

    active_deals = serializers.IntegerField()
    closed_deals = serializers.IntegerField()
    revenue = serializers.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    revenue_change = serializers.CharField()

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "active_deals",
            "closed_deals",
            "revenue",
            "revenue_change",
        ]