from django.urls import path

from .views import ActivityListCreateView


urlpatterns = [
    path(
        "",
        ActivityListCreateView.as_view(),
        name="activity-list-create",
    ),
]