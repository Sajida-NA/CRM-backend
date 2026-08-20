from django.urls import path

from .views import (
    ActivityListCreateView,
    ActivityDetailView,
    ActivityTimelineView,
)

urlpatterns = [

    # Timeline
    path(
        "timeline/<str:module>/<int:object_id>/",
        ActivityTimelineView.as_view(),
        name="activity-timeline",
    ),

    # Get one / Delete one
    path(
        "<int:pk>/",
        ActivityDetailView.as_view(),
        name="activity-detail",
    ),

    # Get all / Create
    path(
        "",
        ActivityListCreateView.as_view(),
        name="activity-list-create",
    ),
]