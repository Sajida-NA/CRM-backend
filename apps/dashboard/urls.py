from django.urls import path

from .views import(
    DashboardSummaryView,
    DashboardConversionView,
    SalesReportView,
    TeamPerformanceView,
)

urlpatterns = [
    path(
        "summary/",
        DashboardSummaryView.as_view(),
        name="dashboard-summary",
    ),

    path(
        "conversion/",
        DashboardConversionView.as_view(),
        name="dashboard-conversion",
    ),

    path(
        "sales-report/",
         SalesReportView.as_view(),
         name="dashboard-sales-report",
    ),

    path(
        "team-performance/",
        TeamPerformanceView.as_view(),
        name="dashboard-team-performance",
    ),
]