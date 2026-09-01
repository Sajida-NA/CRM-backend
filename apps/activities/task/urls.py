# from django.urls import path

# from .views import (
#     TaskListCreateView,
#     TaskDetailView,
# )


# urlpatterns = [

#     # GET all tasks
#     # POST create task
#     path(
#         "",
#         TaskListCreateView.as_view(),
#         name="task-list-create"
#     ),

#     # GET one task
#     # PUT update task
#     # PATCH update task
#     # DELETE delete task
#     path(
#         "<int:pk>/",
#         TaskDetailView.as_view(),
#         name="task-detail"
#     ),
# ]


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