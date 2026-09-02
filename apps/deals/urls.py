# # from django.urls import path

# # from .views import (
# #     DealListCreateView,
# #     DealDetailView,
# # )


# # urlpatterns = [

# #     # GET  -> all deals
# #     # POST -> create deal
# #     path("dealslist/",DealListCreateView.as_view(),name="deals-list-create"),

# #     # GET    -> one deal
# #     # PUT    -> update deal
# #     # PATCH  -> partial update
# #     # DELETE -> delete deal
# #     path("dealslist/<int:pk>/",DealDetailView.as_view(),name="deal-detail"),
# # ]

# from django.urls import path

# from .views import (DealListCreateView, DealDetailView,DealStageListView)


# urlpatterns = [
#     # GET all deals
#     # POST create deal
#     path(
#         "",
#         DealListCreateView.as_view(),
#         name="deals-list-create",
#     ),

#     # GET one deal
#     # PUT update
#     # PATCH partial update
#     # DELETE delete
#     path(
#         "<int:pk>/",
#         DealDetailView.as_view(),
#         name="deal-detail",
#     ),

#      # GET all deal stages
#     path(
#         "stages/",
#         DealStageListView.as_view(),
#         name="deal-stages",
#     ),

# ]


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