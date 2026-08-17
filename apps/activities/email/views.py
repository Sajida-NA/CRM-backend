from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.contrib.contenttypes.models import ContentType

from .models import Email
from .serializers import EmailSerializer

from apps.activities.activity.models import Activity
from apps.leads.models import Lead
from apps.deals.models import Deal


class EmailListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        emails = Email.objects.select_related(
            "activity",
            "activity__created_by"
        ).order_by("-activity__created_at")

        serializer = EmailSerializer(
            emails,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, request):

        object_type = request.data.get("object_type")
        object_id = request.data.get("object_id")

        # Validate object_type
        if object_type not in ["lead", "deal"]:
            return Response(
                {
                    "error": "object_type must be 'lead' or 'deal'."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Select the correct CRM model
        if object_type == "lead":
            model = Lead

        elif object_type == "deal":
            model = Deal

        # Check whether object exists
        try:
            related_object = model.objects.get(
                pk=object_id
            )

        except model.DoesNotExist:
            return Response(
                {
                    "error": f"{object_type} with id {object_id} not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # Get ContentType
        content_type = ContentType.objects.get_for_model(
            model
        )

        # Validate email data first
        serializer = EmailSerializer(
            data=request.data
        )

        if not serializer.is_valid():

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create Activity
        activity = Activity.objects.create(
            activity_type="email",
            created_by=request.user,
            content_type=content_type,
            object_id=related_object.pk
        )

        # Create Email
        email = serializer.save(
            activity=activity
        )

        response_serializer = EmailSerializer(
            email
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )


class EmailDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):

        try:
            return Email.objects.select_related(
                "activity",
                "activity__created_by"
            ).get(pk=pk)

        except Email.DoesNotExist:
            return None

    def get(self, request, pk):

        email = self.get_object(pk)

        if email is None:
            return Response(
                {
                    "detail": "Email not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = EmailSerializer(email)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def put(self, request, pk):

        email = self.get_object(pk)

        if email is None:
            return Response(
                {
                    "detail": "Email not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = EmailSerializer(
            email,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                EmailSerializer(email).data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):

        email = self.get_object(pk)

        if email is None:
            return Response(
                {
                    "detail": "Email not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        email.delete()

        return Response(
            {
                "message": "Email deleted successfully."
            },
            status=status.HTTP_204_NO_CONTENT
        )