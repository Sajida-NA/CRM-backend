from django.urls import path

from .views import (
    MeetingListCreateView,
    MeetingDetailView,
    DealMeetingListView,
    TicketMeetingListView,
    MeetingModuleListView,
)


urlpatterns = [

    # =========================================================
    # GET ALL MEETINGS
    # POST CREATE MEETING
    #
    # /api/activities/meeting/
    # =========================================================

    path(
        "",
        MeetingListCreateView.as_view(),
        name="meeting-list-create",
    ),

    # =========================================================
    # GET MEETINGS FOR ONE DEAL
    #
    # /api/activities/meeting/deal/2/
    # =========================================================

    path(
        "deal/<int:deal_id>/",
        DealMeetingListView.as_view(),
        name="deal-meeting-list",
    ),

    # =========================================================
    # GET MEETINGS FOR ONE TICKET
    #
    # /api/activities/meeting/ticket/5/
    # =========================================================

    path(
        "ticket/<int:ticket_id>/",
        TicketMeetingListView.as_view(),
        name="ticket-meeting-list",
    ),

    # =========================================================
    # GET MEETINGS FOR ANY MODULE
    #
    # /api/activities/meeting/lead/5/
    # /api/activities/meeting/deal/2/
    # /api/activities/meeting/company/4/
    # /api/activities/meeting/ticket/5/
    # =========================================================

    path(
        "<str:module>/<int:module_id>/",
        MeetingModuleListView.as_view(),
        name="meeting-module-list",
    ),

    # =========================================================
    # GET ONE MEETING
    # PUT UPDATE
    # PATCH PARTIAL UPDATE
    # DELETE DELETE
    #
    # /api/activities/meeting/1/
    # =========================================================

    path(
        "<int:pk>/",
        MeetingDetailView.as_view(),
        name="meeting-detail",
    ),
]





