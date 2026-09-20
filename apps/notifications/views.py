from django.shortcuts import render

# Create your views here.
from rest_framework import generics , status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Notification
from .serializers import NotificationSerializer


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            user=self.request.user
        )

class NotificationMarkAsReadView(generics.UpdateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            user=self.request.user
        )

    def update(self, request, *args, **kwargs):
        notification = self.get_object()

        notification.is_read = True
        notification.save()

        serializer = self.get_serializer(notification)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )