

from django.urls import path

from .views import (
    DealListCreateView,
    DealDetailView,
    DealStageListView,
)


urlpatterns = [

    # ==========================================
    # GET all deal stages
    # ==========================================

    path(
        "stages/",
        DealStageListView.as_view(),
        name="deal-stages",
    ),


    # ==========================================
    # GET all deals
    # POST create deal
    # ==========================================

    path(
        "",
        DealListCreateView.as_view(),
        name="deals-list-create",
    ),


    # ==========================================
    # GET one deal
    # PUT update
    # PATCH partial update
    # DELETE delete
    # ==========================================

    path(
        "<int:pk>/",
        DealDetailView.as_view(),
        name="deal-detail",
    ),

]

