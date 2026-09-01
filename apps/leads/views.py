
from django.db import models

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.accounts.models import User

from .models import Lead, Product
from .serializers import (
    LeadListSerializer,
    LeadCreateSerializer,
)


# =========================================================
# LEAD LIST + CREATE
# =========================================================

class LeadListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    # GET - List all leads
    # Also supports Lead Status filtering
    def get(self, request):

        leads = Lead.objects.all().order_by("-created_date")

        # -----------------------------------------
        # GET STATUS FROM URL
        # Example:
        # ?lead_status=Open
        # -----------------------------------------

        lead_status = request.query_params.get(
            "lead_status",
            ""
        ).strip()

        # -----------------------------------------
        # FILTER BY STATUS
        # -----------------------------------------

        if lead_status:
            leads = leads.filter(
                lead_status=lead_status
            )

        # -----------------------------------------
        # SERIALIZE
        # -----------------------------------------

        serializer = LeadListSerializer(
            leads,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    # POST - Create a new lead
    def post(self, request):

        serializer = LeadCreateSerializer(
            data=request.data
        )

        if serializer.is_valid():

            lead = serializer.save()

            response_serializer = LeadListSerializer(
                lead
            )

            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# =========================================================
# SINGLE LEAD DETAIL + UPDATE + DELETE
# =========================================================

class LeadDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):

        try:
            return Lead.objects.prefetch_related(
                "products"
            ).get(pk=pk)

        except Lead.DoesNotExist:
            return None

    # -----------------------------------------
    # GET - Get one lead
    # -----------------------------------------

    def get(self, request, pk):

        lead = self.get_object(pk)

        if lead is None:
            return Response(
                {"detail": "Lead not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = LeadCreateSerializer(
            lead
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    # -----------------------------------------
    # PUT - Update complete lead
    # -----------------------------------------

    def put(self, request, pk):

        lead = self.get_object(pk)

        if lead is None:
            return Response(
                {"detail": "Lead not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = LeadCreateSerializer(
            lead,
            data=request.data
        )

        if serializer.is_valid():

            updated_lead = serializer.save()

            response_serializer = LeadListSerializer(
                updated_lead
            )

            return Response(
                response_serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # -----------------------------------------
    # PATCH - Partially update lead
    # -----------------------------------------

    def patch(self, request, pk):

        lead = self.get_object(pk)

        if lead is None:
            return Response(
                {"detail": "Lead not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = LeadCreateSerializer(
            lead,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            updated_lead = serializer.save()

            response_serializer = LeadListSerializer(
                updated_lead
            )

            return Response(
                response_serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # -----------------------------------------
    # DELETE - Delete lead
    # -----------------------------------------

    def delete(self, request, pk):

        lead = self.get_object(pk)

        if lead is None:
            return Response(
                {"detail": "Lead not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        lead.delete()

        return Response(
            {"detail": "Lead deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )


# =========================================================
# LEAD STATUS DROPDOWN
# =========================================================

class LeadStatusChoicesView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        statuses = [
            {
                "value": value,
                "label": label,
            }
            for value, label in Lead.STATUS_CHOICES
        ]

        return Response(
            statuses,
            status=status.HTTP_200_OK
        )


# =========================================================
# PRODUCTS DROPDOWN
# =========================================================

class ProductListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        products = Product.objects.all().order_by("name")

        product_options = [
            {
                "value": product.id,
                "label": product.name,
            }
            for product in products
        ]

        return Response(
            product_options,
            status=status.HTTP_200_OK
        )


# =========================================================
# COMPANY DROPDOWN
# =========================================================

class LeadCompanyListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        users = User.objects.exclude(
            company_name__isnull=True
        ).exclude(
            company_name=""
        ).values(
            "id",
            "company_name"
        ).distinct().order_by(
            "company_name"
        )

        company_options = [
            {
                "value": user["id"],
                "label": user["company_name"],
            }
            for user in users
        ]

        return Response(
            company_options,
            status=status.HTTP_200_OK
        )