# import traceback

# from django.shortcuts import get_object_or_404

# from rest_framework.views import APIView
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework import status

# from apps.leads.models import Lead
# from apps.deals.models import Deal
# from apps.companies.models import Company
# from apps.tickets.models import Ticket

# from .serializers import AISummarySerializer
# from .services import (
#     build_lead_context,
#     build_deal_context,
#     build_company_context,
#     build_ticket_context,
#     generate_ai_summary,
# )


# class AISummaryView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):

#         serializer = AISummarySerializer(data=request.data)

#         if not serializer.is_valid():
#             return Response(
#                 serializer.errors,
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         module = serializer.validated_data["module"]
#         object_id = serializer.validated_data["object_id"]

#         try:

#             if module == "lead":

#                 lead = get_object_or_404(
#                     Lead,
#                     pk=object_id,
#                 )

#                 context = build_lead_context(lead.id)

#             elif module == "deal":

#                 deal = get_object_or_404(
#                     Deal,
#                     pk=object_id,
#                 )

#                 context = build_deal_context(deal.id)

#             elif module == "company":

#                 company = get_object_or_404(
#                     Company,
#                     pk=object_id,
#                 )

#                 context = build_company_context(company.id)

#             elif module == "ticket":

#                 ticket = get_object_or_404(
#                     Ticket,
#                     pk=object_id,
#                 )

#                 context = build_ticket_context(ticket.id)

#             else:

#                 return Response(
#                     {
#                         "detail": "Unsupported AI summary module."
#                     },
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )

#             summary = generate_ai_summary(
#                 context,
#                 module,
#             )

#             return Response(
#                 {
#                     "module": module,
#                     "object_id": object_id,
#                     "summary": summary,
#                     "data": context,
#                 },
#                 status=status.HTTP_200_OK,
#             )

#         except Exception as exc:

#             print("\n")
#             print("=" * 60)
#             print("AI SUMMARY ERROR")
#             print("=" * 60)
#             print("MODULE:", module)
#             print("OBJECT ID:", object_id)
#             print("ERROR TYPE:", type(exc).__name__)
#             print("ERROR:", str(exc))
#             print("=" * 60)

#             traceback.print_exc()

#             print("=" * 60)
#             print("\n")

#             return Response(
#                 {
#                     "detail": "Failed to generate AI summary.",
#                     "error": str(exc),
#                     "error_type": type(exc).__name__,
#                 },
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             )


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .services import generate_ai_summary


class AISummaryView(APIView):

    def post(self, request):

        try:
            data = request.data.get("data")

            if not data:
                return Response(
                    {
                        "error": "CRM data is required."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            summary = generate_ai_summary(data)

            return Response(
                {
                    "summary": summary
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:

            return Response(
                {
                    "error": "Unable to generate AI summary.",
                    "details": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )