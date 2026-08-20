from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Call
from .serializers import CallSerializer


class CallListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        calls = Call.objects.all().order_by("-created_at")

        serializer = CallSerializer(
            calls,
            many=True,
            context={"request": request}
        )

        return Response(serializer.data)

    def post(self, request):

        serializer = CallSerializer(
            data=request.data,
            context={"request": request}
        )

        if serializer.is_valid():
            call = serializer.save()

            response_serializer = CallSerializer(
                call,
                context={"request": request}
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

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Call.objects.get(pk=pk)
        except Call.DoesNotExist:
            return None

    def get(self, request, pk):

        call = self.get_object(pk)

        if not call:
            return Response(
                {"detail": "Call not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CallSerializer(
            call,
            context={"request": request}
        )

        return Response(serializer.data)

    def put(self, request, pk):

        call = self.get_object(pk)

        if not call:
            return Response(
                {"detail": "Call not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CallSerializer(
            call,
            data=request.data,
            context={"request": request}
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                CallSerializer(
                    call,
                    context={"request": request}
                ).data
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, pk):

        call = self.get_object(pk)

        if not call:
            return Response(
                {"detail": "Call not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CallSerializer(
            call,
            data=request.data,
            partial=True,
            context={"request": request}
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                CallSerializer(
                    call,
                    context={"request": request}
                ).data
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):

        call = self.get_object(pk)

        if not call:
            return Response(
                {"detail": "Call not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        call.delete()

        return Response(
            {"detail": "Call deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )