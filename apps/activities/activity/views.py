from django.contrib.contenttypes.models import ContentType

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Activity
from .serializers import ActivitySerializer


class ActivityListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, module, module_id):

        try:

            content_type = ContentType.objects.get(
                model=module.lower()
            )

        except ContentType.DoesNotExist:

            return Response(
                {
                    "error": f"Invalid module: {module}"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        activities = Activity.objects.filter(
            content_type=content_type,
            object_id=module_id
        ).select_related(
            "created_by",
            "content_type"
        ).order_by(
            "-created_at"
        )

        serializer = ActivitySerializer(
            activities,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class ActivityTypeListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(
        self,
        request,
        module,
        module_id,
        activity_type
    ):

        valid_types = [
            "note",
            "call",
            "task",
            "email",
            "meeting",
        ]

        activity_type = activity_type.lower()

        if activity_type not in valid_types:

            return Response(
                {
                    "error": (
                        f"Invalid activity type: "
                        f"{activity_type}"
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            content_type = ContentType.objects.get(
                model=module.lower()
            )

        except ContentType.DoesNotExist:

            return Response(
                {
                    "error": f"Invalid module: {module}"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        activities = Activity.objects.filter(
            content_type=content_type,
            object_id=module_id,
            activity_type=activity_type
        ).select_related(
            "created_by",
            "content_type"
        ).order_by(
            "-created_at"
        )

        serializer = ActivitySerializer(
            activities,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )