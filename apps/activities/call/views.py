from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.notifications.models import Notification

from .models import Call
from .serializers import CallSerializer


class CallListCreateView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    # =================================================
    # GET ALL CALLS
    # =================================================

    def get(self, request):

        calls = (
            Call.objects
            .select_related(
                "activity",
                "activity__created_by",
                "activity__content_type",
                "connected_content_type",
            )
            .order_by("-created_at")
        )

        serializer = CallSerializer(
            calls,
            many=True,
            context={
                "request": request
            }
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    # =================================================
    # CREATE CALL
    # =================================================

    def post(self, request):

        serializer = CallSerializer(
            data=request.data,
            context={
                "request": request
            }
        )

        if serializer.is_valid():

            call = serializer.save()

            Notification.objects.create(
               user=request.user,
               title="New Call Added",
               message=f"New call has been added for {call.date} at {call.time}.",
            )

            response_serializer = CallSerializer(
                call,
                context={
                    "request": request
                }
            )

            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class CallDetailView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    # =================================================
    # GET CALL OBJECT
    # =================================================

    def get_object(self, pk):

        try:

            return (
                Call.objects
                .select_related(
                    "activity",
                    "activity__created_by",
                    "activity__content_type",
                    "connected_content_type",
                )
                .get(pk=pk)
            )

        except Call.DoesNotExist:

            return None

    # =================================================
    # GET SINGLE CALL
    # =================================================

    def get(self, request, pk):

        call = self.get_object(pk)

        if not call:

            return Response(
                {
                    "detail": "Call not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CallSerializer(
            call,
            context={
                "request": request
            }
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    # =================================================
    # PUT
    # =================================================

    def put(
        self,
        request,
        pk
    ):

        call = self.get_object(pk)

        if not call:

            return Response(
                {
                    "detail": "Call not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CallSerializer(
            call,
            data=request.data,
            context={
                "request": request
            }
        )

        if serializer.is_valid():

            call = serializer.save()

            Notification.objects.create(
                user=request.user,
                title="Call Updated",
                message=f"Call on {call.date} at {call.time} has been updated.",
             )

            response_serializer = CallSerializer(
                call,
                context={
                    "request": request
                }
            )

            return Response(
                response_serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # =================================================
    # PATCH
    # =================================================

    def patch(
        self,
        request,
        pk
    ):

        call = self.get_object(pk)

        if not call:

            return Response(
                {
                    "detail": "Call not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CallSerializer(
            call,
            data=request.data,
            partial=True,
            context={
                "request": request
            }
        )

        if serializer.is_valid():

        

            call = serializer.save()

            Notification.objects.create(
              user=request.user,
              title="Call Updated",
              message=f"Call on {call.date} at {call.time} has been updated.",
            )

            response_serializer = CallSerializer(
                call,
                context={
                    "request": request
                }
            )

            return Response(
                response_serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # =================================================
    # DELETE
    # =================================================

    def delete(
        self,
        request,
        pk
    ):

        call = self.get_object(pk)

        if not call:

            return Response(
                {
                    "detail": "Call not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        call_date = call.date
        call_time = call.time

        Notification.objects.create(
           user=request.user,
           title="Call Deleted",
           message=f"Call scheduled for {call_date} at {call_time} has been deleted.",
)

        call.delete()

        return Response(
            {
                "detail": "Call deleted successfully."
            },
            status=status.HTTP_204_NO_CONTENT
        )