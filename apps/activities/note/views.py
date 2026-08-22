from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Note
from .serializers import NoteSerializer


class NoteListCreateView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    # =================================================
    # GET ALL NOTES
    # =================================================

    def get(self, request):

        notes = (
            Note.objects
            .select_related(
                "activity",
                "activity__created_by",
                "activity__content_type",
            )
            .order_by("-created_at")
        )

        serializer = NoteSerializer(
            notes,
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
    # CREATE NOTE
    # =================================================

    def post(self, request):

        serializer = NoteSerializer(
            data=request.data,
            context={
                "request": request
            }
        )

        if serializer.is_valid():

            note = serializer.save()

            response_serializer = NoteSerializer(
                note,
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


class NoteDetailView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    # =================================================
    # GET NOTE OBJECT
    # =================================================

    def get_object(self, pk):

        try:

            return (
                Note.objects
                .select_related(
                    "activity",
                    "activity__created_by",
                    "activity__content_type",
                )
                .get(pk=pk)
            )

        except Note.DoesNotExist:

            return None

    # =================================================
    # GET SINGLE NOTE
    # =================================================

    def get(
        self,
        request,
        pk
    ):

        note = self.get_object(pk)

        if note is None:

            return Response(
                {
                    "detail": "Note not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = NoteSerializer(
            note,
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

        note = self.get_object(pk)

        if note is None:

            return Response(
                {
                    "detail": "Note not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = NoteSerializer(
            note,
            data=request.data,
            partial=True,
            context={
                "request": request
            }
        )

        if serializer.is_valid():

            serializer.save()

            response_serializer = NoteSerializer(
                note,
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

        note = self.get_object(pk)

        if note is None:

            return Response(
                {
                    "detail": "Note not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = NoteSerializer(
            note,
            data=request.data,
            partial=True,
            context={
                "request": request
            }
        )

        if serializer.is_valid():

            serializer.save()

            response_serializer = NoteSerializer(
                note,
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

        note = self.get_object(pk)

        if note is None:

            return Response(
                {
                    "detail": "Note not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        note.delete()

        return Response(
            {
                "detail": "Note deleted successfully."
            },
            status=status.HTTP_204_NO_CONTENT
        )