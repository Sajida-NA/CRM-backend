from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Activity
from .serializers import ActivitySerializer


class ActivityListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        activities = Activity.objects.all().order_by("-created_at")

        serializer = ActivitySerializer(
            activities,
            many=True,
            context={"request": request}
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = ActivitySerializer(
            data=request.data,
            context={"request": request}
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class ActivityDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Activity.objects.get(pk=pk)
        except Activity.DoesNotExist:
            return None

    def get(self, request, pk):
        activity = self.get_object(pk)

        if activity is None:
            return Response(
                {"error": "Activity not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ActivitySerializer(
            activity,
            context={"request": request}
        )

        return Response(serializer.data)

    def put(self, request, pk):
        activity = self.get_object(pk)

        if activity is None:
            return Response(
                {"error": "Activity not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ActivitySerializer(
            activity,
            data=request.data,
            context={"request": request}
        )

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, pk):
        activity = self.get_object(pk)

        if activity is None:
            return Response(
                {"error": "Activity not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ActivitySerializer(
            activity,
            data=request.data,
            partial=True,
            context={"request": request}
        )

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        activity = self.get_object(pk)

        if activity is None:
            return Response(
                {"error": "Activity not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        activity.delete()

        return Response(
            {"message": "Activity deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )