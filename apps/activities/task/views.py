from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Task
from .serializers import TaskSerializer


class TaskListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    # --------------------------------
    # GET - List all tasks
    # --------------------------------

    def get(self, request):

        tasks = Task.objects.all().order_by("-created_at")

        serializer = TaskSerializer(
            tasks,
            many=True,
            context={"request": request}
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    # --------------------------------
    # POST - Create task
    # --------------------------------

    def post(self, request):

        serializer = TaskSerializer(
            data=request.data,
            context={"request": request}
        )

        if serializer.is_valid():

            task = serializer.save()

            response_serializer = TaskSerializer(
                task,
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


class TaskDetailView(APIView):

    permission_classes = [IsAuthenticated]

    # --------------------------------
    # Get task
    # --------------------------------

    def get_object(self, pk):

        try:
            return Task.objects.get(pk=pk)

        except Task.DoesNotExist:
            return None

    # --------------------------------
    # GET - Single task
    # --------------------------------

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

    # --------------------------------
    # PUT - Full update
    # --------------------------------

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

        if serializer.is_valid():

            task = serializer.save()

            response_serializer = TaskSerializer(
                task,
                context={"request": request}
            )

            return Response(
                response_serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # --------------------------------
    # PATCH - Partial update
    # --------------------------------

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

        if serializer.is_valid():

            task = serializer.save()

            response_serializer = TaskSerializer(
                task,
                context={"request": request}
            )

            return Response(
                response_serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # --------------------------------
    # DELETE - Delete task
    # --------------------------------

    def delete(self, request, pk):

        task = self.get_object(pk)

        if task is None:
            return Response(
                {"detail": "Task not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        task.delete()

        return Response(
            {"detail": "Task deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )