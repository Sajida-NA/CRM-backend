from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Lead
from .serializers import (
    LeadSerializer,
    LeadCreateSerializer,
    LeadListSerializer,
)


class LeadListCreateView(APIView):

    # GET → Display Lead List
    def get(self, request):

        leads = Lead.objects.select_related(
            "user"
        ).all()

        serializer = LeadListSerializer(
            leads,
            many=True
        )

        return Response(
            serializer.data
        )

    # POST → Create Lead
    def post(self, request):

        serializer = LeadCreateSerializer(
            data=request.data
        )

        if serializer.is_valid():

            lead = serializer.save()

            # Return complete Lead after creation
            response_serializer = LeadSerializer(
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


class LeadDetailView(APIView):

    def get_object(self, pk):

        try:

            return Lead.objects.select_related(
                "user"
            ).get(pk=pk)

        except Lead.DoesNotExist:

            return None

    # GET → Get one Lead with all details
    def get(self, request, pk):

        lead = self.get_object(pk)

        if lead is None:

            return Response(
                {"detail": "Lead not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = LeadSerializer(
            lead
        )

        return Response(
            serializer.data
        )

    # PUT → Update complete Lead
    def put(self, request, pk):

        lead = self.get_object(pk)

        if lead is None:

            return Response(
                {"detail": "Lead not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = LeadSerializer(
            lead,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # PATCH → Update partial Lead
    def patch(self, request, pk):

        lead = self.get_object(pk)

        if lead is None:

            return Response(
                {"detail": "Lead not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = LeadSerializer(
            lead,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # DELETE → Delete Lead
    def delete(self, request, pk):

        lead = self.get_object(pk)

        if lead is None:

            return Response(
                {"detail": "Lead not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Keep the User account.
        # Remove only Lead.
        user = lead.user

        lead.delete()

        # Convert Lead user back to normal user
        user.is_lead = False
        user.save(
            update_fields=["is_lead"]
        )

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )