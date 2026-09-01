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



