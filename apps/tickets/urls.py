from django.urls import path

from .views import TicketListCreateView, TicketDetailView

urlpatterns = [
    path("", TicketListCreateView.as_view(), name="ticket-list"),
    path("<int:pk>/", TicketDetailView.as_view(), name="ticket-detail"),
]
