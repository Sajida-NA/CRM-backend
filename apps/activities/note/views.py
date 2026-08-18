# Import Django REST Framework API tools
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Require the user to be authenticated
from rest_framework.permissions import IsAuthenticated

# Import Note model
from .models import Note

# Import Note serializer
from .serializers import NoteSerializer


# List all Notes and create a new Note
class NoteListCreateView(APIView):

    # Only authenticated users can access Notes
    permission_classes = [IsAuthenticated]

    # GET /api/activities/note/
    # Return all Notes, newest first
    def get(self, request):

        # Fetch Notes together with their related Activity
        # and the user who created the Activity
        notes = Note.objects.select_related(
            "activity",
            "activity__created_by",
            "activity__content_type"
        ).order_by("-created_at")

        # Serialize the Notes
        serializer = NoteSerializer(
            notes,
            many=True,
            context={"request": request}
        )

        # Return the serialized Notes
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    # POST /api/activities/note/
    # Create a new Note
    def post(self, request):

        # Validate the incoming Note data
        serializer = NoteSerializer(
            data=request.data,
            context={"request": request}
        )

        # Check validation
        if serializer.is_valid():

            # Create Activity + Note
            note = serializer.save()

            # Serialize the newly created Note
            response_serializer = NoteSerializer(
                note,
                context={"request": request}
            )

            # Return the created Note
            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )

        # Return validation errors
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# Retrieve, update, or delete a single Note
class NoteDetailView(APIView):

    # Only authenticated users can access Notes
    permission_classes = [IsAuthenticated]

    # Find a Note by ID
    def get_object(self, pk):

        try:
            return Note.objects.select_related(
                "activity",
                "activity__created_by",
                "activity__content_type"
            ).get(pk=pk)

        except Note.DoesNotExist:
            return None

    # GET /api/activities/note/<id>/
    # Return one Note
    def get(self, request, pk):

        # Find the Note
        note = self.get_object(pk)

        # Return 404 if it doesn't exist
        if note is None:
            return Response(
                {
                    "detail": "Note not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # Serialize the Note
        serializer = NoteSerializer(
            note,
            context={"request": request}
        )

        # Return the Note
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    # PUT /api/activities/note/<id>/
    # Update a Note
    def put(self, request, pk):

        # Find the Note
        note = self.get_object(pk)

        # Return 404 if it doesn't exist
        if note is None:
            return Response(
                {
                    "detail": "Note not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # Validate updated Note data
        serializer = NoteSerializer(
            note,
            data=request.data,
            partial=True,
            context={"request": request}
        )

        # Check validation
        if serializer.is_valid():

            # Save the changes
            serializer.save()

            # Return updated Note
            return Response(
                NoteSerializer(
                    note,
                    context={"request": request}
                ).data,
                status=status.HTTP_200_OK
            )

        # Return validation errors
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # DELETE /api/activities/note/<id>/
    # Delete a Note
    def delete(self, request, pk):

        # Find the Note
        note = self.get_object(pk)

        # Return 404 if it doesn't exist
        if note is None:
            return Response(
                {
                    "detail": "Note not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # Delete the Note
        # The related Activity will also be deleted
        # because Note.activity uses on_delete=models.CASCADE
        note.delete()

        # Return success response
        return Response(
            {
                "message": "Note deleted successfully."
            },
            status=status.HTTP_204_NO_CONTENT
        )