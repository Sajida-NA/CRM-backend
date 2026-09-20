

from django.urls import path

from .views import (
    LeadListCreateView,
    LeadDetailView,
    LeadStatusChoicesView,
    ProductListView,
    LeadCompanyListView,
)


urlpatterns = [

    # Lead list + create
    path(
        "leadslist/",
        LeadListCreateView.as_view(),
        name="lead-list-create"
    ),

    # Single lead + edit + delete
    path(
        "leadslist/<int:pk>/",
        LeadDetailView.as_view(),
        name="lead-detail"
    ),

    # Dropdowns
    path(
        "lead-statuses/",
        LeadStatusChoicesView.as_view(),
        name="lead-statuses"
    ),

    path(
        "products/",
        ProductListView.as_view(),
        name="products"
    ),

    path(
        "companies/",
        LeadCompanyListView.as_view(),
        name="lead-companies"
    ),
]