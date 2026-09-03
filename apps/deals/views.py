# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated

# from .models import Deal
# from .serializers import (
#     DealCreateSerializer,
#     DealListSerializer,
# )


# class DealListCreateView(APIView):

#     # Only authenticated users can access Deals
#     permission_classes = [IsAuthenticated]

#     # GET - List all deals
#     def get(self, request):

#         deals = Deal.objects.select_related(
#             "associated_lead",
#             "deal_owner"
#         ).all()

#         serializer = DealListSerializer(
#             deals,
#             many=True
#         )

#         return Response(
#             serializer.data,
#             status=status.HTTP_200_OK
#         )

#     # POST - Create a new deal
#     def post(self, request):

#         serializer = DealCreateSerializer(
#             data=request.data
#         )

#         if serializer.is_valid():

#             deal = serializer.save()

#             response_serializer = DealListSerializer(
#                 deal
#             )

#             return Response(
#                 response_serializer.data,
#                 status=status.HTTP_201_CREATED
#             )

#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )



# class DealStageListView(APIView):

#     permission_classes = [IsAuthenticated]

#     def get(self, request):

#         stages = [
#             {
#                 "value": value,
#                 "label": label,
#             }
#             for value, label in Deal.DEAL_STAGE_CHOICES
#         ]

#         return Response(
#             stages,
#             status=status.HTTP_200_OK
#         )

    
# class DealDetailView(APIView):

#     # Only authenticated users can access Deal details
#     permission_classes = [IsAuthenticated]

#     # GET - Get one deal
#     def get(self, request, pk):

#         try:

#             deal = Deal.objects.select_related(
#                 "associated_lead",
#                 "deal_owner"
#             ).get(pk=pk)

#         except Deal.DoesNotExist:

#             return Response(
#                 {
#                     "detail": "Deal not found."
#                 },
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         serializer = DealListSerializer(
#             deal
#         )

#         return Response(
#             serializer.data,
#             status=status.HTTP_200_OK
#         )

#     # PUT - Complete update
#     def put(self, request, pk):

#         try:

#             deal = Deal.objects.select_related(
#                 "associated_lead",
#                 "deal_owner"
#             ).get(pk=pk)

#         except Deal.DoesNotExist:

#             return Response(
#                 {
#                     "detail": "Deal not found."
#                 },
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         serializer = DealCreateSerializer(
#             deal,
#             data=request.data
#         )

#         if serializer.is_valid():

#             deal = serializer.save()

#             response_serializer = DealListSerializer(
#                 deal
#             )

#             return Response(
#                 response_serializer.data,
#                 status=status.HTTP_200_OK
#             )

#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )

#     # PATCH - Partial update
#     def patch(self, request, pk):

#         try:

#             deal = Deal.objects.select_related(
#                 "associated_lead",
#                 "deal_owner"
#             ).get(pk=pk)

#         except Deal.DoesNotExist:

#             return Response(
#                 {
#                     "detail": "Deal not found."
#                 },
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         serializer = DealCreateSerializer(
#             deal,
#             data=request.data,
#             partial=True
#         )

#         if serializer.is_valid():

#             deal = serializer.save()

#             response_serializer = DealListSerializer(
#                 deal
#             )

#             return Response(
#                 response_serializer.data,
#                 status=status.HTTP_200_OK
#             )

#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )

#     # DELETE - Delete deal
#     def delete(self, request, pk):

#         try:

#             deal = Deal.objects.get(pk=pk)

#         except Deal.DoesNotExist:

#             return Response(
#                 {
#                     "detail": "Deal not found."
#                 },
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         deal.delete()

#         return Response(
#             {
#                 "message": "Deal deleted successfully."
#             },
#             status=status.HTTP_204_NO_CONTENT
#         )
# class DealStageListView(APIView):

#     permission_classes = [IsAuthenticated]

#     def get(self, request):

#         stages = [
#             {
#                 "value": value,
#                 "label": label,
#             }
#             for value, label in Deal.DEAL_STAGE_CHOICES
#         ]

#         return Response(
#             stages,
#             status=status.HTTP_200_OK
#         )

from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework import status 
from rest_framework.permissions import IsAuthenticated 
 
from .models import Deal 
from .serializers import ( 
    DealCreateSerializer, 
    DealListSerializer, 
) 
 
 
class DealListCreateView(APIView): 
 
    # Only authenticated users can access Deals 
    permission_classes = [IsAuthenticated] 
 
    # GET - List all deals 
    def get(self, request): 
 
        deals = Deal.objects.select_related( 
            "associated_lead", 
            "deal_owner" 
        ).all() 
 
        serializer = DealListSerializer( 
            deals, 
            many=True 
        ) 
 
        return Response( 
            serializer.data, 
            status=status.HTTP_200_OK 
        ) 
 
    # POST - Create a new deal 
    def post(self, request): 
 
        serializer = DealCreateSerializer( 
            data=request.data 
        ) 
 
        if serializer.is_valid(): 
 
            deal = serializer.save() 
 
            response_serializer = DealListSerializer( 
                deal 
            ) 
 
            return Response( 
                response_serializer.data, 
                status=status.HTTP_201_CREATED 
            ) 
 
        return Response( 
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST 
        ) 
 
 
class DealDetailView(APIView): 
 
    # Only authenticated users can access Deal details 
    permission_classes = [IsAuthenticated] 
 
    # GET - Get one deal 
    def get(self, request, pk): 
 
        try: 
 
            deal = Deal.objects.select_related( 
                "associated_lead", 
                "deal_owner" 
            ).get(pk=pk) 
 
        except Deal.DoesNotExist: 
 
            return Response( 
                { 
                    "detail": "Deal not found." 
                }, 
                status=status.HTTP_404_NOT_FOUND 
            ) 
 
        serializer = DealListSerializer( 
            deal 
        ) 
 
        return Response( 
            serializer.data, 
            status=status.HTTP_200_OK 
        ) 
 
    # PUT - Complete update 
    def put(self, request, pk): 
 
        try: 
 
            deal = Deal.objects.select_related( 
                "associated_lead", 
                "deal_owner" 
            ).get(pk=pk) 
 
        except Deal.DoesNotExist: 
 
            return Response( 
                { 
                    "detail": "Deal not found." 
                }, 
                status=status.HTTP_404_NOT_FOUND 
            ) 
 
        serializer = DealCreateSerializer( 
            deal, 
            data=request.data 
        ) 
 
        if serializer.is_valid(): 
 
            deal = serializer.save() 
 
            response_serializer = DealListSerializer( 
                deal 
            ) 
 
            return Response( 
                response_serializer.data, 
                status=status.HTTP_200_OK 
            ) 
 
        return Response( 
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST 
        ) 
 
    # PATCH - Partial update 
    def patch(self, request, pk): 
 
        try: 
 
            deal = Deal.objects.select_related( 
                "associated_lead", 
                "deal_owner" 
            ).get(pk=pk) 
 
        except Deal.DoesNotExist: 
 
            return Response( 
                { 
                    "detail": "Deal not found." 
                }, 
                status=status.HTTP_404_NOT_FOUND 
            ) 
 
        serializer = DealCreateSerializer( 
            deal, 
            data=request.data, 
            partial=True 
        ) 
 
        if serializer.is_valid(): 
 
            deal = serializer.save() 
 
            response_serializer = DealListSerializer( 
                deal 
            ) 
 
            return Response( 
                response_serializer.data, 
                status=status.HTTP_200_OK 
            ) 
 
        return Response( 
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST 
        ) 
 
    # DELETE - Delete deal 
    def delete(self, request, pk): 
 
        try: 
 
            deal = Deal.objects.get(pk=pk) 
 
        except Deal.DoesNotExist: 
 
            return Response( 
                { 
                    "detail": "Deal not found." 
                }, 
                status=status.HTTP_404_NOT_FOUND 
            ) 
 
        deal.delete() 
 
        return Response( 
            { 
                "message": "Deal deleted successfully." 
            }, 
            status=status.HTTP_204_NO_CONTENT 
        ) 
class DealStageListView(APIView): 
 
    permission_classes = [IsAuthenticated] 
 
    def get(self, request): 
 
        stages = [ 
            { 
                "value": value, 
                "label": label, 
            } 
            for value, label in Deal.DEAL_STAGE_CHOICES 
        ] 
 
        return Response( 
            stages, 
            status=status.HTTP_200_OK 
        )