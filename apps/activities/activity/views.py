from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.contrib.contenttypes.models import ContentType

from .models import Activity
from .serializers import ActivitySerializer


class ActivityListCreateView(APIView):

    permission_classes = [IsAuthenticated]

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
                ActivitySerializer(
                    activity,
                    context={
                        "request": request
                    }
                ).data,
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

        serializer = ActivitySerializer(activity)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

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
            status=status.HTTP_204_NO_CONTENT
        )


# ==========================================================
# ACTIVITY TIMELINE
# ==========================================================

class ActivityTimelineView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, module, object_id):

        allowed_modules = [
            "lead",
            "deal",
            "company",
            "ticket",
        ]

        module = module.lower()

        if module not in allowed_modules:
            return Response(
                {
                    "detail": (
                        f"Choose one of: "
                        f"{', '.join(allowed_modules)}"
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            content_type = ContentType.objects.get(
                model=module
            )

        except ContentType.DoesNotExist:

            return Response(
                {
                    "detail": (
                        f"No model found for module "
                        f"'{module}'."
                    )
                },
                status=status.HTTP_404_NOT_FOUND
            )

        activities = Activity.objects.filter(
            content_type=content_type,
            object_id=object_id
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