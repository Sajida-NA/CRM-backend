from django.urls import path

from .views import (
    CallListCreateView,
    CallDetailView,
)

urlpatterns = [
    path("", CallListCreateView.as_view()),
    path("<int:pk>/", CallDetailView.as_view()),
]