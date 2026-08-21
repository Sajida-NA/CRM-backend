# from django.shortcuts import get_object_or_404

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated

# from .models import Meeting
# from .serializers import MeetingSerializer


# class MeetingListCreateView(APIView):

#     permission_classes = [IsAuthenticated]

#     def get(self, request):

#         meetings = Meeting.objects.all().order_by("-id")

#         serializer = MeetingSerializer(
#             meetings,
#             many=True
#         )

#         return Response(
#             serializer.data,
#             status=status.HTTP_200_OK
#         )

#     def post(self, request):

#         serializer = MeetingSerializer(
#             data=request.data
#         )

#         if serializer.is_valid():

#             serializer.save()

#             return Response(
#                 {
#                     "message": "Meeting created successfully.",
#                     "data": serializer.data
#                 },
#                 status=status.HTTP_201_CREATED
#             )

#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )


# class MeetingDetailView(APIView):

#     permission_classes = [IsAuthenticated]

#     def get(self, request, pk):

#         meeting = get_object_or_404(
#             Meeting,
#             pk=pk
#         )

#         serializer = MeetingSerializer(meeting)

#         return Response(
#             serializer.data,
#             status=status.HTTP_200_OK
#         )

#     def put(self, request, pk):

#         meeting = get_object_or_404(
#             Meeting,
#             pk=pk
#         )

#         serializer = MeetingSerializer(
#             meeting,
#             data=request.data
#         )

#         if serializer.is_valid():

#             serializer.save()

#             return Response(
#                 {
#                     "message": "Meeting updated successfully.",
#                     "data": serializer.data
#                 },
#                 status=status.HTTP_200_OK
#             )

#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )

#     def delete(self, request, pk):

#         meeting = get_object_or_404(
#             Meeting,
#             pk=pk
#         )

#         meeting.delete()

#         return Response(
#             {
#                 "message": "Meeting deleted successfully."
#             },
#             status=status.HTTP_200_OK
#         )

from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Meeting
from .serializers import (
    MeetingSerializer,
    MeetingResponseSerializer,
)


class MeetingListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        meetings = Meeting.objects.all().order_by("-id")

        serializer = MeetingResponseSerializer(
            meetings,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, request):

        serializer = MeetingSerializer(
            data=request.data
        )

        if serializer.is_valid():

            meeting = serializer.save()

            response_serializer = MeetingResponseSerializer(
                meeting
            )

            return Response(
                {
                    "message": "Meeting created successfully.",
                    "data": response_serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class MeetingDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        meeting = get_object_or_404(
            Meeting,
            pk=pk
        )

        serializer = MeetingResponseSerializer(
            meeting
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def put(self, request, pk):

        meeting = get_object_or_404(
            Meeting,
            pk=pk
        )

        serializer = MeetingSerializer(
            meeting,
            data=request.data
        )

        if serializer.is_valid():

            meeting = serializer.save()

            response_serializer = MeetingResponseSerializer(
                meeting
            )

            return Response(
                {
                    "message": "Meeting updated successfully.",
                    "data": response_serializer.data
                },
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, pk):

        meeting = get_object_or_404(
            Meeting,
            pk=pk
        )

        serializer = MeetingSerializer(
            meeting,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            meeting = serializer.save()

            response_serializer = MeetingResponseSerializer(
                meeting
            )

            return Response(
                {
                    "message": "Meeting updated successfully.",
                    "data": response_serializer.data
                },
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):

        meeting = get_object_or_404(
            Meeting,
            pk=pk
        )

        meeting.delete()

        return Response(
            {
                "message": "Meeting deleted successfully."
            },
            status=status.HTTP_200_OK
        )