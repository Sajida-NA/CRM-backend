from django.urls import path

from .views import (
    ActivityListView,
    ActivityTypeListView,
)


urlpatterns = [

    # Get ALL activities
    #
    # /api/activities/lead/5/
    #
    path(
        "<str:module>/<int:module_id>/",
        ActivityListView.as_view(),
        name="activity-list"
    ),

    # Get specific activity type
    #
    # /api/activities/lead/5/note/
    # /api/activities/lead/5/call/
    # /api/activities/lead/5/task/
    #
    path(
        "<str:module>/<int:module_id>/<str:activity_type>/",
        ActivityTypeListView.as_view(),
        name="activity-type-list"
    ),
]