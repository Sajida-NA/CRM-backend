
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Ticket

from apps.notifications.models import Notification

from .serializers import (
    TicketSerializer,
    TicketListSerializer,
    UpdateTicketSerializer,
)


# =====================================================
# TICKET LIST AND CREATE
# =====================================================

class TicketListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        tickets = (
            Ticket.objects
            .select_related("ticket_owner", "associated_deal")
            .all()
            .order_by("-id")
        )

        serializer = TicketListSerializer(tickets, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, request):

        serializer = TicketSerializer(data=request.data)

        if serializer.is_valid():
            ticket = serializer.save()
            Notification.objects.create(
                user=request.user,
                title="New Ticket Added",
                message=f"New ticket {ticket.ticket_name} has been added.",
            )

            return Response(
                {
                    "message": "Ticket created successfully.",
                    "data": TicketListSerializer(ticket).data,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# =====================================================
# TICKET DETAIL / UPDATE / DELETE
# =====================================================

class TicketDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        ticket = get_object_or_404(
            Ticket.objects.select_related(
                "ticket_owner",
                "associated_deal"
            ),
            pk=pk
        )

        serializer = TicketListSerializer(ticket)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def put(self, request, pk):

        ticket = get_object_or_404(Ticket, pk=pk)

        old_status = ticket.ticket_status

        serializer = UpdateTicketSerializer(ticket, data=request.data)

        if serializer.is_valid():
            ticket = serializer.save()

            if old_status != ticket.ticket_status:
              Notification.objects.create(
                user=request.user,
                title="Ticket Status Changed",
                message=(
                    f"Ticket {ticket.ticket_name} moved "
                    f"from {old_status} to {ticket.ticket_status}."
                ),
            )
            else:
              Notification.objects.create(
                user=request.user,
                title="Ticket Updated",
                message=f"Ticket {ticket.ticket_name} has been updated.",
            )

            return Response(
                {
                    "message": "Ticket updated successfully.",
                    "data": TicketListSerializer(ticket).data,
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, pk):

        ticket = get_object_or_404(Ticket, pk=pk)

        old_status = ticket.ticket_status
        
        serializer = UpdateTicketSerializer(ticket, data=request.data, partial=True)

        if serializer.is_valid():
            ticket = serializer.save()

            if old_status != ticket.ticket_status:
                Notification.objects.create(
                    user=request.user,
                    title="Ticket Status Changed",
                    message=(
                       f"Ticket {ticket.ticket_name} moved "
                       f"from {old_status} to {ticket.ticket_status}."
                    ),
                )
            else:
                Notification.objects.create(
                    user=request.user,
                    title="Ticket Updated",
                    message=f"Ticket {ticket.ticket_name} has been updated.",
                )

            return Response(
                {
                    "message": "Ticket updated successfully.",
                    "data": TicketListSerializer(ticket).data,
                },
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, pk):

        ticket = get_object_or_404(Ticket, pk=pk)
        ticket_name = ticket.ticket_name
        ticket.delete()

        Notification.objects.create(
           user=request.user,
           title="Ticket Deleted",
           message=f"Ticket {ticket_name} has been deleted.",
        )

        return Response(
            {
                "message": "Ticket deleted successfully."
            },
            status=status.HTTP_200_OK
        )