"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views.

For more information please see:
https://docs.djangoproject.com/en/6.0/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


# =========================================================
# ROOT
# =========================================================

def home(request):
    return redirect("/admin/")


# =========================================================
# URL PATTERNS
# =========================================================

urlpatterns = [

    # -----------------------------------------------------
    # ROOT
    # -----------------------------------------------------

    path("", home, name="home"),

    # -----------------------------------------------------
    # ADMIN
    # -----------------------------------------------------

    path("admin/", admin.site.urls),

    # -----------------------------------------------------
    # ACCOUNTS
    # -----------------------------------------------------

    path(
        "api/accounts/",
        include("apps.accounts.urls"),
    ),

    # -----------------------------------------------------
    # COMPANIES
    # -----------------------------------------------------

    path(
        "api/",
        include("apps.companies.urls"),
    ),

    # -----------------------------------------------------
    # LEADS
    # -----------------------------------------------------

    path(
        "api/leads/",
        include("apps.leads.urls"),
    ),

    # -----------------------------------------------------
    # DEALS
    # -----------------------------------------------------

    path(
        "api/deals/",
        include("apps.deals.urls"),
    ),

    # -----------------------------------------------------
    # TICKETS
    # -----------------------------------------------------

    path(
        "api/tickets/",
        include("apps.tickets.urls"),
    ),

    # -----------------------------------------------------
    # DASHBOARD
    # -----------------------------------------------------

    path(
        "api/dashboard/",
        include("apps.dashboard.urls"),
    ),

    # -----------------------------------------------------
    # NOTIFICATIONS
    # -----------------------------------------------------

    path(
        "api/notifications/",
        include("apps.notifications.urls"),
    ),

    # -----------------------------------------------------
    # SEARCH
    # -----------------------------------------------------

    path(
        "api/search/",
        include("apps.search.urls"),
    ),

    # =====================================================
    # ACTIVITIES
    # =====================================================

    path(
        "api/activities/activity/",
        include("apps.activities.activity.urls"),
    ),

    path(
        "api/activities/call/",
        include("apps.activities.call.urls"),
    ),

    path(
        "api/activities/email/",
        include("apps.activities.email.urls"),
    ),

    path(
        "api/activities/meeting/",
        include("apps.activities.meeting.urls"),
    ),

    path(
        "api/activities/note/",
        include("apps.activities.note.urls"),
    ),

    path(
        "api/activities/task/",
        include("apps.activities.task.urls"),
    ),

    # =====================================================
    # JWT TOKEN
    # =====================================================

    path(
        "api/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),

    path(
        "api/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),

    # =====================================================
    # AI
    # =====================================================

    path(
        "api/ai/",
        include("apps.ai.urls"),
    ),
]
