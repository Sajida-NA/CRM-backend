
from django.urls import path

from .views import (
    LeadListCreateView,
    LeadDetailView,
)


urlpatterns = [

    # Lead list and create
    path(
        "leadslist/",
        LeadListCreateView.as_view(),
        name="lead-list-create"
    ),

    # Lead detail, update and delete
    path(
        "leadslist/<int:pk>/",
        LeadDetailView.as_view(),
        name="lead-detail"
    ),

]