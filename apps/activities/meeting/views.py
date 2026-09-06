from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.notifications.models import Notification

from .models import Meeting

from .serializers import (
    MeetingSerializer,
    MeetingResponseSerializer,
)


class MeetingListCreateView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    # =====================================================
    # GET ALL MEETINGS
    # =====================================================

    def get(self, request):

        meetings = (
            Meeting.objects
            .select_related(
                "owner",
                "content_type"
            )
            .prefetch_related(
                "attendees"
            )
            .all()
            .order_by("-id")
        )

        serializer = MeetingResponseSerializer(
            meetings,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    # =====================================================
    # POST
    # =====================================================

    def post(self, request):

        serializer = MeetingSerializer(
            data=request.data
        )

        if serializer.is_valid():

            meeting = serializer.save()

            Notification.objects.create(
               user=request.user,
               title="New Meeting Added",
               message=f"Meeting {meeting.title} has been created.",
            )

            response_serializer = (
                MeetingResponseSerializer(
                    meeting
                )
            )

            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class MeetingDetailView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    # =====================================================
    # GET SINGLE
    # =====================================================

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

    # =====================================================
    # PUT
    # =====================================================

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

            Notification.objects.create(
               user=request.user,
               title="Meeting Updated",
               message=f"Meeting {meeting.title} has been updated.",
            )

            response_serializer = (
                MeetingResponseSerializer(
                    meeting
                )
            )

            return Response(
                response_serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # =====================================================
    # PATCH
    # =====================================================

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

            Notification.objects.create(
               user=request.user,
               title="Meeting Updated",
               message=f"Meeting {meeting.title} has been updated.",
            )

            response_serializer = (
                MeetingResponseSerializer(
                    meeting
                )
            )

            return Response(
                response_serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # =====================================================
    # DELETE
    # =====================================================

    def delete(self, request, pk):

        meeting = get_object_or_404(
            Meeting,
            pk=pk
        )

        meeting_title = meeting.title

        meeting.delete()

        Notification.objects.create(
           user=request.user,
           title="Meeting Deleted",
           message=f"Meeting {meeting_title} has been deleted.",
        )

        return Response(
            {
                "message": "Meeting deleted successfully."
            },
            status=status.HTTP_200_OK
        )