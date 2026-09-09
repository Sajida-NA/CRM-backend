# from django.urls import path

# from .views import (
#     CallListCreateView,
#     CallDetailView,
# )


# urlpatterns = [

#     path(
#         "",
#         CallListCreateView.as_view(),
#         name="call-list-create"
#     ),

#     path(
#         "<int:pk>/",
#         CallDetailView.as_view(),
#         name="call-detail"
#     ),
# ]

# from django.urls import path

# from .views import (
#     CallListCreateView,
#     CallDetailView,
#     StartCallView,
#     TwilioVoiceWebhookView,
# )

# urlpatterns = [
#     path("", CallListCreateView.as_view(), name="call-list-create"),
#     path("start/", StartCallView.as_view(), name="call-start"),
#     path(
#         "twilio/voice/",
#         TwilioVoiceWebhookView.as_view(),
#         name="twilio-voice-webhook",
#     ),
#     path("<int:pk>/", CallDetailView.as_view(), name="call-detail"),
# ]


from django.urls import path

from .views import (
    CallListCreateView,
    CallDetailView,
    StartCallView,
    SyncCallView,
)


urlpatterns = [

    # =========================================================
    # GET ALL CALLS
    # POST NORMAL CALL
    #
    # /api/activities/call/
    # =========================================================

    path(
        "",
        CallListCreateView.as_view(),
        name="call-list-create",
    ),

    # =========================================================
    # START TWILIO CALL
    #
    # POST
    # /api/activities/call/start/
    # =========================================================

    path(
        "start/",
        StartCallView.as_view(),
        name="call-start",
    ),

    # =========================================================
    # SYNC TWILIO STATUS / DURATION / OUTCOME
    #
    # GET
    # /api/activities/call/<id>/sync/
    # =========================================================

    path(
        "<int:pk>/sync/",
        SyncCallView.as_view(),
        name="call-sync",
    ),

    # =========================================================
    # GET / UPDATE / DELETE CALL
    #
    # /api/activities/call/<id>/
    # =========================================================

    path(
        "<int:pk>/",
        CallDetailView.as_view(),
        name="call-detail",
    ),
]