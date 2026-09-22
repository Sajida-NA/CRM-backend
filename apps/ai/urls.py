from django.urls import path

from .views import AISummaryView


urlpatterns = [
    path(
        "summary/",
        AISummaryView.as_view(),
        name="ai-summary",
    ),
]