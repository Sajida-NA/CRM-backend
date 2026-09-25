

# from django.urls import path

# from .views import (
#     DealListCreateView,
#     DealDetailView,
#     DealStageListView,
# )


# urlpatterns = [

#     # ==========================================
#     # GET all deal stages
#     # ==========================================

#     path(
#         "stages/",
#         DealStageListView.as_view(),
#         name="deal-stages",
#     ),


#     # ==========================================
#     # GET all deals
#     # POST create deal
#     # ==========================================

#     path(
#         "",
#         DealListCreateView.as_view(),
#         name="deals-list-create",
#     ),


#     # ==========================================
#     # GET one deal
#     # PUT update
#     # PATCH partial update
#     # DELETE delete
#     # ==========================================

#     path(
#         "<int:pk>/",
#         DealDetailView.as_view(),
#         name="deal-detail",
#     ),

# ]




from django.urls import path

from .views import (
    DealListCreateView,
    DealOwnerListView,
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
    # GET all Deal Owners
    #
    # Used for Ticket Owner selection.
    # Returns only users who are assigned
    # to at least one Deal.
    # ==========================================

    path(
        "owners/",
        DealOwnerListView.as_view(),
        name="deal-owners",
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

