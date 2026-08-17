from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Lead
from .serializers import (
    LeadListSerializer,
    LeadCreateSerializer,
)


class LeadListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    # GET - List all leads
    def get(self, request):

        leads = Lead.objects.prefetch_related("products").all()

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

            # Return the lead using the list serializer
            response_serializer = LeadListSerializer(lead)

            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class LeadDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):

        try:
            return Lead.objects.prefetch_related(
                "products"
            ).get(pk=pk)

        except Lead.DoesNotExist:
            return None

    # GET - Get one lead
    def get(self, request, pk):

        lead = self.get_object(pk)

        if lead is None:
            return Response(
                {"detail": "Lead not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = LeadListSerializer(lead)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    # PUT - Update complete lead
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

            lead = serializer.save()

            response_serializer = LeadListSerializer(lead)

            return Response(
                response_serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # PATCH - Partially update lead
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

            lead = serializer.save()

            response_serializer = LeadListSerializer(lead)

            return Response(
                response_serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # DELETE - Delete lead
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