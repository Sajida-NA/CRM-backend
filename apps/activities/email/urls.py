from django.urls import path

from .views import (
    EmailListCreateView,
    EmailDetailView
)


urlpatterns = [

    path(
        "",
        EmailListCreateView.as_view(),
        name="email-list-create"
    ),

    path(
        "<int:pk>/",
        EmailDetailView.as_view(),
        name="email-detail"
    ),
]