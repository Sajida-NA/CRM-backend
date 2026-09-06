from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Task
from .serializers import TaskSerializer

from apps.notifications.models import Notification


class TaskListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        tasks = (
            Task.objects
            .select_related(
                "activity",
                "activity__created_by",
                "assigned_to",
                "content_type"
            )
            .all()
            .order_by("-created_at")
        )

        serializer = TaskSerializer(
            tasks,
            many=True,
            context={"request": request}
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, request):

        serializer = TaskSerializer(
            data=request.data,
            context={"request": request}
        )

        serializer.is_valid(raise_exception=True)

        task = serializer.save()

        Notification.objects.create(
           user=request.user,
           title="New Task Added",
           message=f"Task {task.title} has been created.",
        )

        return Response(
            TaskSerializer(
                task,
                context={"request": request}
            ).data,
            status=status.HTTP_201_CREATED
        )


class TaskDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):

        try:
            return Task.objects.get(pk=pk)

        except Task.DoesNotExist:
            return None

    def get(self, request, pk):

        task = self.get_object(pk)

        if task is None:
            return Response(
                {"detail": "Task not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TaskSerializer(
            task,
            context={"request": request}
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def put(self, request, pk):

        task = self.get_object(pk)

        if task is None:
            return Response(
                {"detail": "Task not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TaskSerializer(
            task,
            data=request.data,
            context={"request": request}
        )

        serializer.is_valid(raise_exception=True)

        task = serializer.save()

        Notification.objects.create(
           user=request.user,
           title="Task Updated",
           message=f"Task {task.title} has been updated.",
        )

        return Response(
            TaskSerializer(
                task,
                context={"request": request}
            ).data,
            status=status.HTTP_200_OK
        )

    def patch(self, request, pk):

        task = self.get_object(pk)

        if task is None:
            return Response(
                {"detail": "Task not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TaskSerializer(
            task,
            data=request.data,
            partial=True,
            context={"request": request}
        )

        serializer.is_valid(raise_exception=True)

        task = serializer.save()

        Notification.objects.create(
           user=request.user,
           title="Task Updated",
           message=f"Task {task.title} has been updated.",
        )

        return Response(
            TaskSerializer(
                task,
                context={"request": request}
            ).data,
            status=status.HTTP_200_OK
        )

    def delete(self, request, pk):

        task = self.get_object(pk)

        if task is None:
            return Response(
                {"detail": "Task not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        task_title = task.title

        task.delete()

        Notification.objects.create(
           user=request.user,
           title="Task Deleted",
           message=f"Task {task_title} has been deleted.",
        )

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )