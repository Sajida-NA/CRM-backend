

from django.urls import path

from .views import (
    TaskListCreateView,
    TaskDetailView,
    TaskOptionsView,
)


urlpatterns = [

    # GET all tasks
    # POST create task
    path(
        "",
        TaskListCreateView.as_view(),
        name="task-list-create",
    ),

    # GET task options
    path(
        "options/",
        TaskOptionsView.as_view(),
        name="task-options",
    ),

    # GET one
    # PUT
    # PATCH
    # DELETE
    path(
        "<int:pk>/",
        TaskDetailView.as_view(),
        name="task-detail",
    ),
]