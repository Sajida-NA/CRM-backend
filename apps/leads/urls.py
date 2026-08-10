
from django.urls import path

from .views import (LeadListCreateView,LeadDetailView,)


urlpatterns = [

    # List + Create
    path("leadslist/",LeadListCreateView.as_view(),name="leads-list-create"),

    # Get + Update + Delete
    path("leadslist/<int:pk>/",LeadDetailView.as_view(),name="lead-detail"),

    # path("leads/",LeadCreateView.as_view(),name="lead-create"),
]