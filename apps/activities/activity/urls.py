

# from django.urls import path

# from .views import (
#     ActivityTimelineView,
#     ActivityTypeDetailView,
# )


# urlpatterns = [

#     # =================================================
#     # GET ALL ACTIVITIES FOR A MODULE RECORD
#     #
#     # /api/activities/lead/4/
#     # /api/activities/deal/4/
#     # /api/activities/company/4/
#     # /api/activities/ticket/4/
#     # =================================================

#     path(
#         "<str:module>/<int:module_id>/",
#         ActivityTimelineView.as_view(),
#         name="activity-timeline",
#     ),

#     # =================================================
#     # GET ACTIVITIES OF ONE TYPE
#     #
#     # /api/activities/lead/4/note/
#     # /api/activities/lead/4/call/
#     # /api/activities/lead/4/task/
#     # /api/activities/lead/4/meeting/
#     # /api/activities/lead/4/email/
#     # =================================================

#     path(
#         "<str:module>/<int:module_id>/<str:activity_type>/",
#         ActivityTypeDetailView.as_view(),
#         name="activity-type-detail",
#     ),
# ]


from django.urls import path 
 
from .views import ActivityTimelineView,ActivityTypeDetailView 
 
 
urlpatterns = [ 
 
    path( 
        "<str:module>/<int:module_id>/", 
        ActivityTimelineView.as_view(), 
        name="activity-timeline" 
    ), 
 
 
    # GET activities of one type 
    path( 
        "<str:module>/<int:module_id>/<str:activity_type>/", 
        ActivityTypeDetailView.as_view(), 
        name="activity-type-detail" 
    ), 
 
] 
