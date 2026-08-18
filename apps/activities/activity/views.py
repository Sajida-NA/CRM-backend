from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.contrib.contenttypes.models import ContentType

from .models import Activity
from .serializers import ActivitySerializer


class ActivityListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    # ==========================================
    # GET ALL ACTIVITIES
    # ==========================================

    def get(self, request):

        activities = Activity.objects.select_related(
            "created_by",
            "content_type"
        ).order_by("-created_at")

        serializer = ActivitySerializer(
            activities,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    # ==========================================
    # CREATE ACTIVITY
    # ==========================================

    def post(self, request):

        serializer = ActivitySerializer(
            data=request.data,
            context={
                "request": request
            }
        )

        if serializer.is_valid():

            activity = serializer.save()

            return Response(
                ActivitySerializer(activity).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class ActivityDetailView(APIView):

    permission_classes = [IsAuthenticated]

    # ==========================================
    # GET ACTIVITY
    # ==========================================

    def get_object(self, pk):

        try:

            return Activity.objects.select_related(
                "created_by",
                "content_type"
            ).get(pk=pk)

        except Activity.DoesNotExist:

            return None

    def get(self, request, pk):

        activity = self.get_object(pk)

        if activity is None:

            return Response(
                {
                    "detail": "Activity not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ActivitySerializer(
            activity
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    # ==========================================
    # DELETE
    # ==========================================

    def delete(self, request, pk):

        activity = self.get_object(pk)

        if activity is None:

            return Response(
                {
                    "detail": "Activity not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        activity.delete()

        return Response(
            {
                "message": "Activity deleted successfully."
            },
            status=status.HTTP_204_NO_CONTENT
        )