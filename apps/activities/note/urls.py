# Import Django's URL path function
from django.urls import path

# Import Note API views
from .views import (
    NoteListCreateView,
    NoteDetailView,
)


# Note API URL patterns
urlpatterns = [

    # List all Notes / Create a new Note
    # GET  /api/activities/note/
    # POST /api/activities/note/
    path(
        "",
        NoteListCreateView.as_view(),
        name="note-list-create"
    ),

    # Retrieve / Update / Delete a specific Note
    # GET    /api/activities/note/<id>/
    # PUT    /api/activities/note/<id>/
    # DELETE /api/activities/note/<id>/
    path(
        "<int:pk>/",
        NoteDetailView.as_view(),
        name="note-detail"
    ),
]