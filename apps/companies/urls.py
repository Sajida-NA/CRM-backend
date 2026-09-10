

from django.urls import path

from .views import CompanyListCreateView, CompanyDetailView

urlpatterns = [
    path(
        "companies/",
        CompanyListCreateView.as_view(),
        name="company-list",
    ),

    path(
        "companies/<int:pk>/",
        CompanyDetailView.as_view(),
        name="company-detail",
    ),
]
