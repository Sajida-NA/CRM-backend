# from django.shortcuts import get_object_or_404

# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework.views import APIView

# from .models import Ticket

# from apps.notifications.models import Notification

# from .serializers import (
#     TicketSerializer,
#     TicketListSerializer,
#     UpdateTicketSerializer,
# )


# # =====================================================
# # TICKET LIST AND CREATE
# # =====================================================

# class TicketListCreateView(APIView):

#     permission_classes = [IsAuthenticated]

#     def get(self, request):

#         tickets = (
#             Ticket.objects
#             .select_related("associated_deal")
#             .prefetch_related("ticket_owners")
#             .all()
#             .order_by("-id")
#         )

#         serializer = TicketListSerializer(
#             tickets,
#             many=True
#         )

#         return Response(
#             serializer.data,
#             status=status.HTTP_200_OK
#         )

#     def post(self, request):

#         serializer = TicketSerializer(
#             data=request.data
#         )

#         if serializer.is_valid():
#             ticket = serializer.save()

#             Notification.objects.create(
#                 user=request.user,
#                 title="New Ticket Added",
#                 message=(
#                     f"New ticket {ticket.ticket_name} "
#                     f"has been added."
#                 ),
#             )

#             return Response(
#                 {
#                     "message": "Ticket created successfully.",
#                     "data": TicketListSerializer(ticket).data,
#                 },
#                 status=status.HTTP_201_CREATED,
#             )

#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )


# # =====================================================
# # TICKET DETAIL / UPDATE / DELETE
# # =====================================================

# class TicketDetailView(APIView):

#     permission_classes = [IsAuthenticated]

#     def get_ticket(self, pk):
#         return get_object_or_404(
#             Ticket.objects
#             .select_related("associated_deal")
#             .prefetch_related("ticket_owners"),
#             pk=pk
#         )

#     # =================================================
#     # GET TICKET
#     # =================================================

#     def get(self, request, pk):

#         ticket = self.get_ticket(pk)

#         serializer = TicketListSerializer(ticket)

#         return Response(
#             serializer.data,
#             status=status.HTTP_200_OK
#         )

#     # =================================================
#     # UPDATE TICKET
#     # =================================================

#     def put(self, request, pk):

#         ticket = self.get_ticket(pk)

#         old_status = ticket.ticket_status

#         serializer = UpdateTicketSerializer(
#             ticket,
#             data=request.data
#         )

#         if serializer.is_valid():

#             ticket = serializer.save()

#             if old_status != ticket.ticket_status:

#                 Notification.objects.create(
#                     user=request.user,
#                     title="Ticket Status Changed",
#                     message=(
#                         f"Ticket {ticket.ticket_name} moved "
#                         f"from {old_status} to "
#                         f"{ticket.ticket_status}."
#                     ),
#                 )

#             else:

#                 Notification.objects.create(
#                     user=request.user,
#                     title="Ticket Updated",
#                     message=(
#                         f"Ticket {ticket.ticket_name} "
#                         f"has been updated."
#                     ),
#                 )

#             # Reload M2M relationship for response
#             ticket = self.get_ticket(pk)

#             return Response(
#                 {
#                     "message": "Ticket updated successfully.",
#                     "data": TicketListSerializer(ticket).data,
#                 },
#                 status=status.HTTP_200_OK,
#             )

#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )

#     # =================================================
#     # PATCH TICKET
#     # =================================================

#     def patch(self, request, pk):

#         ticket = self.get_ticket(pk)

#         old_status = ticket.ticket_status

#         serializer = UpdateTicketSerializer(
#             ticket,
#             data=request.data,
#             partial=True
#         )

#         if serializer.is_valid():

#             ticket = serializer.save()

#             if old_status != ticket.ticket_status:

#                 Notification.objects.create(
#                     user=request.user,
#                     title="Ticket Status Changed",
#                     message=(
#                         f"Ticket {ticket.ticket_name} moved "
#                         f"from {old_status} to "
#                         f"{ticket.ticket_status}."
#                     ),
#                 )

#             else:

#                 Notification.objects.create(
#                     user=request.user,
#                     title="Ticket Updated",
#                     message=(
#                         f"Ticket {ticket.ticket_name} "
#                         f"has been updated."
#                     ),
#                 )

#             # Reload M2M relationship for response
#             ticket = self.get_ticket(pk)

#             return Response(
#                 {
#                     "message": "Ticket updated successfully.",
#                     "data": TicketListSerializer(ticket).data,
#                 },
#                 status=status.HTTP_200_OK,
#             )

#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )

#     # =================================================
#     # DELETE TICKET
#     # =================================================

#     def delete(self, request, pk):

#         ticket = get_object_or_404(
#             Ticket,
#             pk=pk
#         )

#         ticket_name = ticket.ticket_name

#         ticket.delete()

#         Notification.objects.create(
#             user=request.user,
#             title="Ticket Deleted",
#             message=(
#                 f"Ticket {ticket_name} "
#                 f"has been deleted."
#             ),
#         )

#         return Response(
#             {
#                 "message": "Ticket deleted successfully."
#             },
#             status=status.HTTP_200_OK
#         )





# from django.shortcuts import get_object_or_404

# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework.views import APIView

# from .models import Ticket

# from apps.notifications.models import Notification

# from .serializers import (
#     TicketSerializer,
#     TicketListSerializer,
#     UpdateTicketSerializer,
# )


# # =====================================================
# # TICKET LIST AND CREATE
# # =====================================================

# class TicketListCreateView(APIView):

#     permission_classes = [IsAuthenticated]

#     def get(self, request):

#         tickets = (
#             Ticket.objects
#             .select_related(
#                 "associated_deal",
#                 "associated_deal__associated_lead",
#             )
#             .prefetch_related("ticket_owners")
#             .all()
#             .order_by("-id")
#         )

#         serializer = TicketListSerializer(
#             tickets,
#             many=True
#         )

#         return Response(
#             serializer.data,
#             status=status.HTTP_200_OK
#         )

#     def post(self, request):

#         serializer = TicketSerializer(
#             data=request.data
#         )

#         if serializer.is_valid():
#             ticket = serializer.save()

#             Notification.objects.create(
#                 user=request.user,
#                 title="New Ticket Added",
#                 message=(
#                     f"New ticket {ticket.ticket_name} "
#                     f"has been added."
#                 ),
#             )

#             # Reload related Deal + Lead
#             ticket = (
#                 Ticket.objects
#                 .select_related(
#                     "associated_deal",
#                     "associated_deal__associated_lead",
#                 )
#                 .prefetch_related("ticket_owners")
#                 .get(pk=ticket.pk)
#             )

#             return Response(
#                 {
#                     "message": "Ticket created successfully.",
#                     "data": TicketListSerializer(ticket).data,
#                 },
#                 status=status.HTTP_201_CREATED,
#             )

#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )


# # =====================================================
# # TICKET DETAIL / UPDATE / DELETE
# # =====================================================

# class TicketDetailView(APIView):

#     permission_classes = [IsAuthenticated]

#     def get_ticket(self, pk):

#         return get_object_or_404(
#             Ticket.objects
#             .select_related(
#                 "associated_deal",
#                 "associated_deal__associated_lead",
#             )
#             .prefetch_related("ticket_owners"),
#             pk=pk
#         )

#     # =================================================
#     # GET TICKET
#     # =================================================

#     def get(self, request, pk):

#         ticket = self.get_ticket(pk)

#         serializer = TicketListSerializer(ticket)

#         return Response(
#             serializer.data,
#             status=status.HTTP_200_OK
#         )

#     # =================================================
#     # UPDATE TICKET
#     # =================================================

#     def put(self, request, pk):

#         ticket = self.get_ticket(pk)

#         old_status = ticket.ticket_status

#         serializer = UpdateTicketSerializer(
#             ticket,
#             data=request.data
#         )

#         if serializer.is_valid():

#             ticket = serializer.save()

#             if old_status != ticket.ticket_status:

#                 Notification.objects.create(
#                     user=request.user,
#                     title="Ticket Status Changed",
#                     message=(
#                         f"Ticket {ticket.ticket_name} moved "
#                         f"from {old_status} to "
#                         f"{ticket.ticket_status}."
#                     ),
#                 )

#             else:

#                 Notification.objects.create(
#                     user=request.user,
#                     title="Ticket Updated",
#                     message=(
#                         f"Ticket {ticket.ticket_name} "
#                         f"has been updated."
#                     ),
#                 )

#             # Reload Deal + Lead + M2M relationships
#             ticket = self.get_ticket(pk)

#             return Response(
#                 {
#                     "message": "Ticket updated successfully.",
#                     "data": TicketListSerializer(ticket).data,
#                 },
#                 status=status.HTTP_200_OK,
#             )

#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )

#     # =================================================
#     # PATCH TICKET
#     # =================================================

#     def patch(self, request, pk):

#         ticket = self.get_ticket(pk)

#         old_status = ticket.ticket_status

#         serializer = UpdateTicketSerializer(
#             ticket,
#             data=request.data,
#             partial=True
#         )

#         if serializer.is_valid():

#             ticket = serializer.save()

#             if old_status != ticket.ticket_status:

#                 Notification.objects.create(
#                     user=request.user,
#                     title="Ticket Status Changed",
#                     message=(
#                         f"Ticket {ticket.ticket_name} moved "
#                         f"from {old_status} to "
#                         f"{ticket.ticket_status}."
#                     ),
#                 )

#             else:

#                 Notification.objects.create(
#                     user=request.user,
#                     title="Ticket Updated",
#                     message=(
#                         f"Ticket {ticket.ticket_name} "
#                         f"has been updated."
#                     ),
#                 )

#             # Reload Deal + Lead + M2M relationships
#             ticket = self.get_ticket(pk)

#             return Response(
#                 {
#                     "message": "Ticket updated successfully.",
#                     "data": TicketListSerializer(ticket).data,
#                 },
#                 status=status.HTTP_200_OK,
#             )

#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )

#     # =================================================
#     # DELETE TICKET
#     # =================================================

#     def delete(self, request, pk):

#         ticket = get_object_or_404(
#             Ticket,
#             pk=pk
#         )

#         ticket_name = ticket.ticket_name

#         ticket.delete()

#         Notification.objects.create(
#             user=request.user,
#             title="Ticket Deleted",
#             message=(
#                 f"Ticket {ticket_name} "
#                 f"has been deleted."
#             ),
#         )

#         return Response(
#             {
#                 "message": "Ticket deleted successfully."
#             },
#             status=status.HTTP_200_OK
#         )


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
# ADMIN CHECK
# =====================================================

def is_admin(user):
    return (
        str(getattr(user, "role", "")).strip().lower() == "admin"
    )


# =====================================================
# TICKET LIST AND CREATE
# =====================================================

class TicketListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        # =================================================
        # ADMIN → ALL TICKETS
        # USER → ONLY THEIR OWN TICKETS
        # =================================================

        if is_admin(request.user):

            tickets = Ticket.objects.all()

        else:

            tickets = Ticket.objects.filter(
                ticket_owners=request.user
            ).distinct()

        # =================================================
        # RELATED DATA
        # =================================================

        tickets = (
            tickets
            .select_related(
                "associated_deal",
                "associated_deal__associated_lead",
            )
            .prefetch_related("ticket_owners")
            .order_by("-id")
        )

        serializer = TicketListSerializer(
            tickets,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    # =================================================
    # CREATE TICKET
    # =================================================

    def post(self, request):

        serializer = TicketSerializer(
            data=request.data
        )

        if serializer.is_valid():

            ticket = serializer.save()

            Notification.objects.create(
                user=request.user,
                title="New Ticket Added",
                message=(
                    f"New ticket {ticket.ticket_name} "
                    f"has been added."
                ),
            )

            # Reload related Deal + Lead + M2M
            ticket = (
                Ticket.objects
                .select_related(
                    "associated_deal",
                    "associated_deal__associated_lead",
                )
                .prefetch_related("ticket_owners")
                .get(pk=ticket.pk)
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

    # =================================================
    # GET TICKET WITH ACCESS CONTROL
    # =================================================

    def get_ticket(self, pk, user):

        # -------------------------------------------------
        # ADMIN → CAN ACCESS ANY TICKET
        # -------------------------------------------------

        if is_admin(user):

            return get_object_or_404(
                Ticket.objects
                .select_related(
                    "associated_deal",
                    "associated_deal__associated_lead",
                )
                .prefetch_related("ticket_owners"),
                pk=pk
            )

        # -------------------------------------------------
        # NORMAL USER → ONLY THEIR OWN TICKETS
        # -------------------------------------------------

        return get_object_or_404(
            Ticket.objects
            .select_related(
                "associated_deal",
                "associated_deal__associated_lead",
            )
            .prefetch_related("ticket_owners"),
            pk=pk,
            ticket_owners=user
        )

    # =================================================
    # GET TICKET
    # =================================================

    def get(self, request, pk):

        ticket = self.get_ticket(
            pk,
            request.user
        )

        serializer = TicketListSerializer(ticket)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    # =================================================
    # UPDATE TICKET
    # =================================================

    def put(self, request, pk):

        ticket = self.get_ticket(
            pk,
            request.user
        )

        old_status = ticket.ticket_status

        serializer = UpdateTicketSerializer(
            ticket,
            data=request.data
        )

        if serializer.is_valid():

            ticket = serializer.save()

            if old_status != ticket.ticket_status:

                Notification.objects.create(
                    user=request.user,
                    title="Ticket Status Changed",
                    message=(
                        f"Ticket {ticket.ticket_name} moved "
                        f"from {old_status} to "
                        f"{ticket.ticket_status}."
                    ),
                )

            else:

                Notification.objects.create(
                    user=request.user,
                    title="Ticket Updated",
                    message=(
                        f"Ticket {ticket.ticket_name} "
                        f"has been updated."
                    ),
                )

            # Reload Deal + Lead + M2M relationships
            ticket = self.get_ticket(
                pk,
                request.user
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

    # =================================================
    # PATCH TICKET
    # =================================================

    def patch(self, request, pk):

        ticket = self.get_ticket(
            pk,
            request.user
        )

        old_status = ticket.ticket_status

        serializer = UpdateTicketSerializer(
            ticket,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            ticket = serializer.save()

            if old_status != ticket.ticket_status:

                Notification.objects.create(
                    user=request.user,
                    title="Ticket Status Changed",
                    message=(
                        f"Ticket {ticket.ticket_name} moved "
                        f"from {old_status} to "
                        f"{ticket.ticket_status}."
                    ),
                )

            else:

                Notification.objects.create(
                    user=request.user,
                    title="Ticket Updated",
                    message=(
                        f"Ticket {ticket.ticket_name} "
                        f"has been updated."
                    ),
                )

            # Reload Deal + Lead + M2M relationships
            ticket = self.get_ticket(
                pk,
                request.user
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

    # =================================================
    # DELETE TICKET
    # =================================================

    def delete(self, request, pk):

        # -------------------------------------------------
        # ADMIN → ANY TICKET
        # USER → ONLY THEIR OWN TICKET
        # -------------------------------------------------

        ticket = self.get_ticket(
            pk,
            request.user
        )

        ticket_name = ticket.ticket_name

        ticket.delete()

        Notification.objects.create(
            user=request.user,
            title="Ticket Deleted",
            message=(
                f"Ticket {ticket_name} "
                f"has been deleted."
            ),
        )

        return Response(
            {
                "message": "Ticket deleted successfully."
            },
            status=status.HTTP_200_OK
        )