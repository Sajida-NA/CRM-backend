# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated

# from .models import Task
# from .serializers import TaskSerializer


# class TaskListCreateView(APIView):

#     permission_classes = [IsAuthenticated]

#     def get(self, request):

#         tasks = (
#             Task.objects
#             .select_related(
#                 "activity",
#                 "activity__created_by",
#                 "assigned_to",
#                 "content_type"
#             )
#             .all()
#             .order_by("-created_at")
#         )

#         serializer = TaskSerializer(
#             tasks,
#             many=True,
#             context={"request": request}
#         )

#         return Response(
#             serializer.data,
#             status=status.HTTP_200_OK
#         )

#     def post(self, request):

#         serializer = TaskSerializer(
#             data=request.data,
#             context={"request": request}
#         )

#         serializer.is_valid(raise_exception=True)

#         task = serializer.save()

#         return Response(
#             TaskSerializer(
#                 task,
#                 context={"request": request}
#             ).data,
#             status=status.HTTP_201_CREATED
#         )


# class TaskDetailView(APIView):

#     permission_classes = [IsAuthenticated]

#     def get_object(self, pk):

#         try:
#             return Task.objects.get(pk=pk)

#         except Task.DoesNotExist:
#             return None

#     def get(self, request, pk):

#         task = self.get_object(pk)

#         if task is None:
#             return Response(
#                 {"detail": "Task not found."},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         serializer = TaskSerializer(
#             task,
#             context={"request": request}
#         )

#         return Response(
#             serializer.data,
#             status=status.HTTP_200_OK
#         )

#     def put(self, request, pk):

#         task = self.get_object(pk)

#         if task is None:
#             return Response(
#                 {"detail": "Task not found."},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         serializer = TaskSerializer(
#             task,
#             data=request.data,
#             context={"request": request}
#         )

#         serializer.is_valid(raise_exception=True)

#         task = serializer.save()

#         return Response(
#             TaskSerializer(
#                 task,
#                 context={"request": request}
#             ).data,
#             status=status.HTTP_200_OK
#         )

#     def patch(self, request, pk):

#         task = self.get_object(pk)

#         if task is None:
#             return Response(
#                 {"detail": "Task not found."},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         serializer = TaskSerializer(
#             task,
#             data=request.data,
#             partial=True,
#             context={"request": request}
#         )

#         serializer.is_valid(raise_exception=True)

#         task = serializer.save()

#         return Response(
#             TaskSerializer(
#                 task,
#                 context={"request": request}
#             ).data,
#             status=status.HTTP_200_OK
#         )

#     def delete(self, request, pk):

#         task = self.get_object(pk)

#         if task is None:
#             return Response(
#                 {"detail": "Task not found."},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         task.delete()

#         return Response(
#             status=status.HTTP_204_NO_CONTENT
#         )
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model

from .models import Task
from .serializers import TaskSerializer


# ========================================
# LIST + CREATE TASK
# ========================================

class TaskListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    # ====================================
    # GET ALL TASKS
    # ====================================

    def get(self, request):

        tasks = (
            Task.objects
            .select_related(
                "activity",
                "activity__created_by",
                "activity__content_type",
                "assigned_to",
            )
            .all()
            .order_by("-created_at")
        )

        serializer = TaskSerializer(
            tasks,
            many=True,
            context={"request": request},
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    # ====================================
    # POST CREATE TASK
    # ====================================

    def post(self, request):

        serializer = TaskSerializer(
            data=request.data,
            context={"request": request},
        )

        serializer.is_valid(
            raise_exception=True
        )

        task = serializer.save()

        response_serializer = TaskSerializer(
            task,
            context={"request": request},
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )


# ========================================
# TASK OPTIONS
# ========================================

class TaskOptionsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        User = get_user_model()

        # ====================================
        # TASK TYPES
        # ====================================

        task_types = [
            {
                "value": value,
                "label": label,
            }
            for value, label
            in Task.TASK_TYPE_CHOICES
        ]

        # ====================================
        # PRIORITIES
        # ====================================

        priorities = [
            {
                "value": value,
                "label": label,
            }
            for value, label
            in Task.PRIORITY_CHOICES
        ]

        # ====================================
        # USERS
        # ====================================

        users = (
            User.objects
            .filter(is_active=True)
            .order_by(
                "first_name",
                "last_name",
            )
        )

        assigned_users = [
            {
                "id": user.id,
                "name": (
                    user.get_full_name()
                    or user.email
                ),
            }
            for user in users
        ]

        return Response(
            {
                "task_types": task_types,
                "priorities": priorities,
                "assigned_users": assigned_users,
            },
            status=status.HTTP_200_OK,
        )


# ========================================
# TASK DETAIL
# ========================================

class TaskDetailView(APIView):

    permission_classes = [IsAuthenticated]

    # ====================================
    # GET OBJECT
    # ====================================

    def get_object(self, pk):

        try:

            return (
                Task.objects
                .select_related(
                    "activity",
                    "activity__created_by",
                    "activity__content_type",
                    "assigned_to",
                )
                .get(pk=pk)
            )

        except Task.DoesNotExist:

            return None

    # ====================================
    # GET ONE TASK
    # ====================================

    def get(self, request, pk):

        task = self.get_object(pk)

        if task is None:

            return Response(
                {
                    "detail": "Task not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = TaskSerializer(
            task,
            context={"request": request},
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    # ====================================
    # PUT
    # ====================================

    def put(self, request, pk):

        task = self.get_object(pk)

        if task is None:

            return Response(
                {
                    "detail": "Task not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = TaskSerializer(
            task,
            data=request.data,
            context={"request": request},
        )

        serializer.is_valid(
            raise_exception=True
        )

        task = serializer.save()

        return Response(
            TaskSerializer(
                task,
                context={"request": request},
            ).data,
            status=status.HTTP_200_OK,
        )

    # ====================================
    # PATCH
    # ====================================

    def patch(self, request, pk):

        task = self.get_object(pk)

        if task is None:

            return Response(
                {
                    "detail": "Task not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = TaskSerializer(
            task,
            data=request.data,
            partial=True,
            context={"request": request},
        )

        serializer.is_valid(
            raise_exception=True
        )

        task = serializer.save()

        return Response(
            TaskSerializer(
                task,
                context={"request": request},
            ).data,
            status=status.HTTP_200_OK,
        )

    # ====================================
    # DELETE
    # ====================================

    def delete(self, request, pk):

        task = self.get_object(pk)

        if task is None:

            return Response(
                {
                    "detail": "Task not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        task.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )