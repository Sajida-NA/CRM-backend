    

# from django.urls import path

# from .views import (
#     EmailListCreateView,
#     EmailDetailView,
#     EmailRecipientView,
# )


# urlpatterns = [

#     # ==========================================
#     # EMAIL LIST + CREATE
#     # ==========================================

#     path(
#         "",
#         EmailListCreateView.as_view(),
#         name="email-list-create",
#     ),


#     # ==========================================
#     # GET AUTOMATIC RECIPIENT
#     # IMPORTANT: Put this BEFORE <int:pk>/
#     # ==========================================

#     path(
#         "recipient/<str:module>/<int:object_id>/",
#         EmailRecipientView.as_view(),
#         name="email-recipient",
#     ),


#     # ==========================================
#     # EMAIL DETAIL
#     # ==========================================

#     path(
#         "<int:pk>/",
#         EmailDetailView.as_view(),
#         name="email-detail",
#     ),

# ]




from django.urls import path

from .views import (
    EmailListCreateView,
    EmailDetailView,
    EmailRecipientView,
)


urlpatterns = [

    # ==========================================
    # EMAIL LIST + CREATE
    # ==========================================

    path(
        "",
        EmailListCreateView.as_view(),
        name="email-list-create",
    ),


    # ==========================================
    # GET AUTOMATIC RECIPIENT
    # ==========================================

    path(
        "recipient/",
        EmailRecipientView.as_view(),
        name="email-recipient",
    ),


    # ==========================================
    # EMAIL DETAIL
    # ==========================================

    path(
        "<int:pk>/",
        EmailDetailView.as_view(),
        name="email-detail",
    ),

]


