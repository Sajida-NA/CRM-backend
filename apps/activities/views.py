from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Activity
from .serializers import ActivitySerializer


class ActivityListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        activities = Activity.objects.all()

        content_type = request.query_params.get("content_type")
        object_id = request.query_params.get("object_id")

        if content_type and object_id:
            activities = activities.filter(
                content_type_id=content_type,
                object_id=object_id,
            )

        activities = activities.order_by("-created_at")

        serializer = ActivitySerializer(
            activities,
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        serializer = ActivitySerializer(
            data=request.data,
        )

        if serializer.is_valid():
            serializer.save(
                created_by=request.user
            )

            return Response(
                {
                    "message": "Activity created successfully.",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )