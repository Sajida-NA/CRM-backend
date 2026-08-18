from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Meeting
from .serializers import MeetingSerializer


class MeetingListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    # GET
    def get(self, request):
        meetings = Meeting.objects.all().order_by("-id")

        serializer = MeetingSerializer(
            meetings,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    # POST
    def post(self, request):
        serializer = MeetingSerializer(
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "message": "Meeting created successfully.",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class MeetingDetailView(APIView):
    permission_classes = [IsAuthenticated]

    # GET
    def get(self, request, pk):
        meeting = get_object_or_404(
            Meeting,
            pk=pk
        )

        serializer = MeetingSerializer(meeting)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    # PUT 
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
            serializer.save()

            return Response(
                {
                    "message": "Meeting updated successfully.",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # DELETE
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