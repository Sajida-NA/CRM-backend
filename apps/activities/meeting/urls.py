
# from django.urls import path

# from .views import (
#     MeetingListCreateView,
#     MeetingDetailView,
#     DealMeetingListView,
# )


# urlpatterns = [

#     # =========================================================
#     # GET ALL MEETINGS
#     # POST CREATE MEETING
#     # =========================================================

#     path(
#         "",
#         MeetingListCreateView.as_view(),
#         name="meeting-list-create",
#     ),

#     # =========================================================
#     # GET MEETINGS FOR ONE DEAL
#     #
#     # /api/activities/meeting/deal/2/
#     # =========================================================

#     path(
#         "deal/<int:deal_id>/",
#         DealMeetingListView.as_view(),
#         name="deal-meeting-list",
#     ),

#     # =========================================================
#     # GET    ONE MEETING
#     # PUT    UPDATE
#     # PATCH  PARTIAL UPDATE
#     # DELETE DELETE
#     #
#     # /api/activities/meeting/1/
#     # =========================================================

#     path(
#         "<int:pk>/",
#         MeetingDetailView.as_view(),
#         name="meeting-detail",
#     ),
# ]


from django.urls import path 
 
from .views import ( 
    MeetingListCreateView, 
    MeetingDetailView, 
    DealMeetingListView, 
) 
 
 
urlpatterns = [ 
 
    # ========================================================= 
    # GET ALL MEETINGS 
    # POST CREATE MEETING 
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
    # GET    ONE MEETING 
    # PUT    UPDATE 
    # PATCH  PARTIAL UPDATE 
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