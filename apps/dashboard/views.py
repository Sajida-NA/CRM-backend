from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .services import (
    get_dashboard_summary,
    get_conversion_data,
    get_sales_report,
    get_team_performance,
)

from .serializers import (
    DashboardSummarySerializer,
    DashboardConversionSerializer,
    SalesReportSerializer,
    TeamPerformanceSerializer,
)



class DashboardSummaryView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        data = get_dashboard_summary()

        serializer = DashboardSummarySerializer(data)

        return Response(serializer.data)


class DashboardConversionView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        data = get_conversion_data()

        serializer = DashboardConversionSerializer(data)

        return Response(serializer.data)


class SalesReportView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        data = get_sales_report()

        serializer = SalesReportSerializer(
            data,
            many=True
        )

        return Response(serializer.data)


class TeamPerformanceView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        data = get_team_performance()

        serializer = TeamPerformanceSerializer(
            data,
            many=True
        )

        return Response(serializer.data)