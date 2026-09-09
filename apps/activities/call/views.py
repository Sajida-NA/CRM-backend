# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated

# from .models import Call
# from .serializers import CallSerializer


# class CallListCreateView(APIView):

#     permission_classes = [
#         IsAuthenticated
#     ]

#     # =================================================
#     # GET ALL CALLS
#     # =================================================

#     def get(self, request):

#         calls = (
#             Call.objects
#             .select_related(
#                 "activity",
#                 "activity__created_by",
#                 "activity__content_type",
#                 "connected_content_type",
#             )
#             .order_by("-created_at")
#         )

#         serializer = CallSerializer(
#             calls,
#             many=True,
#             context={
#                 "request": request
#             }
#         )

#         return Response(
#             serializer.data,
#             status=status.HTTP_200_OK
#         )

#     # =================================================
#     # CREATE CALL
#     # =================================================

#     def post(self, request):

#         serializer = CallSerializer(
#             data=request.data,
#             context={
#                 "request": request
#             }
#         )

#         if serializer.is_valid():

#             call = serializer.save()

#             response_serializer = CallSerializer(
#                 call,
#                 context={
#                     "request": request
#                 }
#             )

#             return Response(
#                 response_serializer.data,
#                 status=status.HTTP_201_CREATED
#             )

#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )


# class CallDetailView(APIView):

#     permission_classes = [
#         IsAuthenticated
#     ]

#     # =================================================
#     # GET CALL OBJECT
#     # =================================================

#     def get_object(self, pk):

#         try:

#             return (
#                 Call.objects
#                 .select_related(
#                     "activity",
#                     "activity__created_by",
#                     "activity__content_type",
#                     "connected_content_type",
#                 )
#                 .get(pk=pk)
#             )

#         except Call.DoesNotExist:

#             return None

#     # =================================================
#     # GET SINGLE CALL
#     # =================================================

#     def get(self, request, pk):

#         call = self.get_object(pk)

#         if not call:

#             return Response(
#                 {
#                     "detail": "Call not found."
#                 },
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         serializer = CallSerializer(
#             call,
#             context={
#                 "request": request
#             }
#         )

#         return Response(
#             serializer.data,
#             status=status.HTTP_200_OK
#         )

#     # =================================================
#     # PUT
#     # =================================================

#     def put(
#         self,
#         request,
#         pk
#     ):

#         call = self.get_object(pk)

#         if not call:

#             return Response(
#                 {
#                     "detail": "Call not found."
#                 },
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         serializer = CallSerializer(
#             call,
#             data=request.data,
#             context={
#                 "request": request
#             }
#         )

#         if serializer.is_valid():

#             serializer.save()

#             response_serializer = CallSerializer(
#                 call,
#                 context={
#                     "request": request
#                 }
#             )

#             return Response(
#                 response_serializer.data,
#                 status=status.HTTP_200_OK
#             )

#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )

#     # =================================================
#     # PATCH
#     # =================================================

#     def patch(
#         self,
#         request,
#         pk
#     ):

#         call = self.get_object(pk)

#         if not call:

#             return Response(
#                 {
#                     "detail": "Call not found."
#                 },
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         serializer = CallSerializer(
#             call,
#             data=request.data,
#             partial=True,
#             context={
#                 "request": request
#             }
#         )

#         if serializer.is_valid():

#             serializer.save()

#             response_serializer = CallSerializer(
#                 call,
#                 context={
#                     "request": request
#                 }
#             )

#             return Response(
#                 response_serializer.data,
#                 status=status.HTTP_200_OK
#             )

#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )

#     # =================================================
#     # DELETE
#     # =================================================

#     def delete(
#         self,
#         request,
#         pk
#     ):

#         call = self.get_object(pk)

#         if not call:

#             return Response(
#                 {
#                     "detail": "Call not found."
#                 },
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         call.delete()

#         return Response(
#             {
#                 "detail": "Call deleted successfully."
#             },
#             status=status.HTTP_204_NO_CONTENT
#         )















# from django.conf import settings
# from django.contrib.contenttypes.models import ContentType
# from django.http import HttpResponse

# from rest_framework.views import APIView
# from rest_framework.permissions import IsAuthenticated, AllowAny
# from rest_framework.response import Response
# from rest_framework import status

# from twilio.rest import Client
# from twilio.twiml.voice_response import VoiceResponse, Dial

# from .models import Call
# from .serializers import CallSerializer


# MODULE_MAP = {
#     "lead": ("leads", "lead"),
#     "company": ("companies", "company"),
#     "deal": ("deals", "deal"),
#     "ticket": ("tickets", "ticket"),
# }


# # ============================================================
# # GET ALL CALLS
# # POST CREATE CALL
# # ============================================================

# class CallListCreateView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         calls = Call.objects.select_related(
#             "activity",
#             "activity__created_by",
#             "connected_content_type",
#         ).order_by("-created_at")

#         serializer = CallSerializer(
#             calls,
#             many=True,
#         )

#         return Response(serializer.data)

#     def post(self, request):
#         serializer = CallSerializer(
#             data=request.data
#         )

#         if serializer.is_valid():
#             call = serializer.save()

#             return Response(
#                 CallSerializer(call).data,
#                 status=status.HTTP_201_CREATED,
#             )

#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST,
#         )


# # ============================================================
# # START TWILIO TRIAL CALL
# # ============================================================

# class StartCallView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         module = request.data.get("module")
#         module_id = request.data.get("module_id")

#         print("\n================================")
#         print("START TWILIO TRIAL CALL")
#         print("================================")
#         print("Module:", module)
#         print("Module ID:", module_id)

#         # ----------------------------------------------------
#         # Validate module
#         # ----------------------------------------------------

#         if module not in MODULE_MAP:
#             return Response(
#                 {
#                     "detail": "Invalid module."
#                 },
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         if not module_id:
#             return Response(
#                 {
#                     "detail": "module_id is required."
#                 },
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         # ----------------------------------------------------
#         # Get module object
#         # ----------------------------------------------------

#         app_label, model_name = MODULE_MAP[module]

#         try:
#             content_type = ContentType.objects.get(
#                 app_label=app_label,
#                 model=model_name,
#             )

#             model_class = content_type.model_class()

#             obj = model_class.objects.get(
#                 pk=module_id
#             )

#         except ContentType.DoesNotExist:
#             return Response(
#                 {
#                     "detail": "Module configuration not found."
#                 },
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         except model_class.DoesNotExist:
#             return Response(
#                 {
#                     "detail": f"{module.title()} not found."
#                 },
#                 status=status.HTTP_404_NOT_FOUND,
#             )

#         # ----------------------------------------------------
#         # Get customer phone
#         # ----------------------------------------------------

#         customer_phone = None

#         for field in [
#             "phone_number",
#             "phone",
#             "mobile_number",
#             "mobile",
#         ]:
#             value = getattr(obj, field, None)

#             if value:
#                 customer_phone = str(value)
#                 break

#         print("Customer phone:", customer_phone)

#         if not customer_phone:
#             return Response(
#                 {
#                     "detail": "Customer phone number not found."
#                 },
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         # ----------------------------------------------------
#         # Twilio settings
#         # ----------------------------------------------------

#         account_sid = settings.TWILIO_ACCOUNT_SID
#         auth_token = settings.TWILIO_AUTH_TOKEN
#         twilio_phone = settings.TWILIO_PHONE_NUMBER

#         if not account_sid:
#             return Response(
#                 {
#                     "detail": "TWILIO_ACCOUNT_SID is not configured."
#                 },
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             )

#         if not auth_token:
#             return Response(
#                 {
#                     "detail": "TWILIO_AUTH_TOKEN is not configured."
#                 },
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             )

#         if not twilio_phone:
#             return Response(
#                 {
#                     "detail": "TWILIO_PHONE_NUMBER is not configured."
#                 },
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             )

#         # ----------------------------------------------------
#         # TRIAL TEST
#         #
#         # Do NOT use your ngrok webhook here.
#         # ----------------------------------------------------

#         trial_webhook_url = (
#             "https://webhooks.twilio.com/v1/Voice/Template/"
#             "voice_text_to_speech"
#         )

#         try:
#             client = Client(
#                 account_sid,
#                 auth_token,
#             )

#             call = client.calls.create(
#                 to=customer_phone,
#                 from_=twilio_phone,
#                 url=trial_webhook_url,
#             )

#             print("\n================================")
#             print("TWILIO TRIAL CALL CREATED")
#             print("================================")
#             print("Call SID:", call.sid)
#             print("Status:", call.status)
#             print("To:", customer_phone)
#             print("From:", twilio_phone)
#             print("================================\n")

#             return Response(
#                 {
#                     "success": True,
#                     "message": "Twilio trial call started.",
#                     "call_sid": call.sid,
#                     "status": call.status,
#                     "to": customer_phone,
#                     "from": twilio_phone,
#                 },
#                 status=status.HTTP_200_OK,
#             )

#         except Exception as e:
#             print("\n================================================")
#             print("TWILIO TRIAL CALL ERROR")
#             print("================================================")
#             print(str(e))
#             print("================================================\n")

#             return Response(
#                 {
#                     "success": False,
#                     "detail": "Twilio trial call could not be started.",
#                     "error": str(e),
#                 },
#                 status=status.HTTP_502_BAD_GATEWAY,
#             )


# # ============================================================
# # TWILIO VOICE WEBHOOK
# #
# # This is kept because your existing URL still uses it.
# # It will be used later for the CRM-user -> customer bridge.
# # ============================================================

# class TwilioVoiceWebhookView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         response = VoiceResponse()

#         response.say(
#             "Connecting you to the customer."
#         )

#         # This endpoint is currently kept for the future
#         # custom Twilio bridge implementation.

#         return HttpResponse(
#             str(response),
#             content_type="text/xml",
#         )

#     def get(self, request):
#         return self.post(request)


# # ============================================================
# # GET / UPDATE / DELETE SINGLE CALL
# # ============================================================

# class CallDetailView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get_object(self, pk):
#         try:
#             return Call.objects.select_related(
#                 "activity",
#                 "activity__created_by",
#                 "connected_content_type",
#             ).get(pk=pk)

#         except Call.DoesNotExist:
#             return None

#     def get(self, request, pk):
#         call = self.get_object(pk)

#         if not call:
#             return Response(
#                 {
#                     "detail": "Call not found."
#                 },
#                 status=status.HTTP_404_NOT_FOUND,
#             )

#         serializer = CallSerializer(call)

#         return Response(serializer.data)

#     def put(self, request, pk):
#         call = self.get_object(pk)

#         if not call:
#             return Response(
#                 {
#                     "detail": "Call not found."
#                 },
#                 status=status.HTTP_404_NOT_FOUND,
#             )

#         serializer = CallSerializer(
#             call,
#             data=request.data,
#         )

#         if serializer.is_valid():
#             serializer.save()

#             return Response(
#                 serializer.data
#             )

#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST,
#         )

#     def patch(self, request, pk):
#         call = self.get_object(pk)

#         if not call:
#             return Response(
#                 {
#                     "detail": "Call not found."
#                 },
#                 status=status.HTTP_404_NOT_FOUND,
#             )

#         serializer = CallSerializer(
#             call,
#             data=request.data,
#             partial=True,
#         )

#         if serializer.is_valid():
#             serializer.save()

#             return Response(
#                 serializer.data
#             )

#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST,
#         )

#     def delete(self, request, pk):
#         call = self.get_object(pk)

#         if not call:
#             return Response(
#                 {
#                     "detail": "Call not found."
#                 },
#                 status=status.HTTP_404_NOT_FOUND,
#             )

#         call.delete()

#         return Response(
#             {
#                 "message": "Call deleted successfully."
#             },
#             status=status.HTTP_204_NO_CONTENT,
#         )





# from django.conf import settings
# from django.contrib.contenttypes.models import ContentType
# from django.http import HttpResponse

# from rest_framework.views import APIView
# from rest_framework.permissions import IsAuthenticated, AllowAny
# from rest_framework.response import Response
# from rest_framework import status

# from twilio.rest import Client
# from twilio.twiml.voice_response import VoiceResponse, Dial

# from .models import Call
# from .serializers import CallSerializer


# MODULE_MAP = {
#     "lead": ("leads", "lead"),
#     "company": ("companies", "company"),
#     "deal": ("deals", "deal"),
#     "ticket": ("tickets", "ticket"),
# }


# class CallListCreateView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         calls = Call.objects.select_related(
#             "activity",
#             "activity__created_by",
#             "connected_content_type",
#         ).order_by("-created_at")

#         serializer = CallSerializer(calls, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = CallSerializer(data=request.data)

#         if serializer.is_valid():
#             call = serializer.save()

#             return Response(
#                 CallSerializer(call).data,
#                 status=status.HTTP_201_CREATED,
#             )

#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST,
#         )


# class StartCallView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         module = request.data.get("module")
#         module_id = request.data.get("module_id")

#         print("\n================================")
#         print("START SERVER SIDE TWILIO CALL")
#         print("================================")
#         print("Module:", module)
#         print("Module ID:", module_id)

#         # -----------------------------------------
#         # VALIDATE MODULE
#         # -----------------------------------------
#         if module not in MODULE_MAP:
#             return Response(
#                 {"detail": "Invalid module."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         if not module_id:
#             return Response(
#                 {"detail": "module_id is required."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         # -----------------------------------------
#         # GET CUSTOMER / LEAD OBJECT
#         # -----------------------------------------
#         app_label, model_name = MODULE_MAP[module]

#         try:
#             content_type = ContentType.objects.get(
#                 app_label=app_label,
#                 model=model_name,
#             )

#             model_class = content_type.model_class()

#             obj = model_class.objects.get(pk=module_id)

#         except ContentType.DoesNotExist:
#             return Response(
#                 {"detail": "Module configuration not found."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         except model_class.DoesNotExist:
#             return Response(
#                 {
#                     "detail": f"{module.title()} not found."
#                 },
#                 status=status.HTTP_404_NOT_FOUND,
#             )

#         # -----------------------------------------
#         # GET CUSTOMER PHONE
#         # -----------------------------------------
#         customer_phone = None

#         for field in [
#             "phone_number",
#             "phone",
#             "mobile_number",
#             "mobile",
#         ]:
#             value = getattr(obj, field, None)

#             if value:
#                 customer_phone = str(value)
#                 break

#         print("Customer phone:", customer_phone)

#         if not customer_phone:
#             return Response(
#                 {
#                     "detail": "Customer phone number not found."
#                 },
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         # -----------------------------------------
#         # GET LOGGED-IN CRM USER PHONE
#         # -----------------------------------------
#         user_phone = getattr(
#             request.user,
#             "phone_number",
#             None,
#         )

#         print("CRM user:", request.user)
#         print("CRM user phone:", user_phone)

#         if not user_phone:
#             return Response(
#                 {
#                     "detail": "CRM user's phone number not found."
#                 },
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         # -----------------------------------------
#         # TWILIO SETTINGS
#         # -----------------------------------------
#         account_sid = settings.TWILIO_ACCOUNT_SID
#         auth_token = settings.TWILIO_AUTH_TOKEN
#         twilio_phone = settings.TWILIO_PHONE_NUMBER
#         webhook_base_url = (
#             settings.TWILIO_VOICE_WEBHOOK_BASE_URL
#         )

#         if not account_sid:
#             return Response(
#                 {
#                     "detail": "TWILIO_ACCOUNT_SID is not configured."
#                 },
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             )

#         if not auth_token:
#             return Response(
#                 {
#                     "detail": "TWILIO_AUTH_TOKEN is not configured."
#                 },
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             )

#         if not twilio_phone:
#             return Response(
#                 {
#                     "detail": "TWILIO_PHONE_NUMBER is not configured."
#                 },
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             )

#         if not webhook_base_url:
#             return Response(
#                 {
#                     "detail": (
#                         "TWILIO_VOICE_WEBHOOK_BASE_URL "
#                         "is not configured."
#                     )
#                 },
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             )

#         # -----------------------------------------
#         # WEBHOOK URL
#         # -----------------------------------------
#         webhook_url = (
#             f"{webhook_base_url}"
#             f"/api/activities/call/twilio/voice/"
#             f"?customer_phone={customer_phone}"
#         )

#         print("Webhook URL:", webhook_url)

#         # -----------------------------------------
#         # CREATE TWILIO CALL
#         #
#         # IMPORTANT:
#         # First call CRM USER
#         # -----------------------------------------
#         try:
#             client = Client(
#                 account_sid,
#                 auth_token,
#             )

#             call = client.calls.create(
#                 to=user_phone,
#                 from_=twilio_phone,
#                 url=webhook_url,
#                 method="POST",
#             )

#             print("\n================================")
#             print("TWILIO CALL CREATED")
#             print("================================")
#             print("Call SID:", call.sid)
#             print("Status:", call.status)
#             print("CRM User:", user_phone)
#             print("Customer:", customer_phone)
#             print("================================\n")

#             return Response(
#                 {
#                     "success": True,
#                     "message": (
#                         "Call started. "
#                         "CRM user will receive the call first."
#                     ),
#                     "call_sid": call.sid,
#                     "status": call.status,
#                     "user_phone": user_phone,
#                     "customer_phone": customer_phone,
#                 },
#                 status=status.HTTP_200_OK,
#             )

#         except Exception as e:

#             print("\n================================================")
#             print("TWILIO CALL ERROR")
#             print("================================================")
#             print(str(e))
#             print("================================================\n")

#             return Response(
#                 {
#                     "success": False,
#                     "detail": (
#                         "Twilio call could not be started."
#                     ),
#                     "error": str(e),
#                 },
#                 status=status.HTTP_502_BAD_GATEWAY,
#             )


# class TwilioVoiceWebhookView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):

#         customer_phone = request.query_params.get(
#             "customer_phone"
#         )

#         print("\n================================")
#         print("TWILIO WEBHOOK HIT")
#         print("================================")
#         print("Customer phone:", customer_phone)

#         response = VoiceResponse()

#         if not customer_phone:
#             response.say(
#                 "Customer phone number is missing."
#             )

#             return HttpResponse(
#                 str(response),
#                 content_type="text/xml",
#             )

#         # -----------------------------------------
#         # CONNECT CRM USER TO CUSTOMER
#         # -----------------------------------------
#         response.say(
#             "Connecting you to the customer."
#         )

#         dial = Dial(
#             timeout=30,
#             caller_id=settings.TWILIO_PHONE_NUMBER,
#         )

#         dial.number(customer_phone)

#         response.append(dial)

#         print("Dialing customer:", customer_phone)
#         print("================================\n")

#         return HttpResponse(
#             str(response),
#             content_type="text/xml",
#         )

#     def get(self, request):
#         return self.post(request)


# class CallDetailView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get_object(self, pk):

#         try:
#             return Call.objects.select_related(
#                 "activity",
#                 "activity__created_by",
#                 "connected_content_type",
#             ).get(pk=pk)

#         except Call.DoesNotExist:
#             return None

#     def get(self, request, pk):

#         call = self.get_object(pk)

#         if not call:
#             return Response(
#                 {"detail": "Call not found."},
#                 status=status.HTTP_404_NOT_FOUND,
#             )

#         serializer = CallSerializer(call)

#         return Response(serializer.data)

#     def put(self, request, pk):

#         call = self.get_object(pk)

#         if not call:
#             return Response(
#                 {"detail": "Call not found."},
#                 status=status.HTTP_404_NOT_FOUND,
#             )

#         serializer = CallSerializer(
#             call,
#             data=request.data,
#         )

#         if serializer.is_valid():
#             serializer.save()

#             return Response(serializer.data)

#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST,
#         )

#     def patch(self, request, pk):

#         call = self.get_object(pk)

#         if not call:
#             return Response(
#                 {"detail": "Call not found."},
#                 status=status.HTTP_404_NOT_FOUND,
#             )

#         serializer = CallSerializer(
#             call,
#             data=request.data,
#             partial=True,
#         )

#         if serializer.is_valid():
#             serializer.save()

#             return Response(serializer.data)

#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST,
#         )

#     def delete(self, request, pk):

#         call = self.get_object(pk)

#         if not call:
#             return Response(
#                 {"detail": "Call not found."},
#                 status=status.HTTP_404_NOT_FOUND,
#             )

#         call.delete()

#         return Response(
#             {"message": "Call deleted successfully."},
#             status=status.HTTP_204_NO_CONTENT,
#         )


import logging

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import transaction

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from twilio.rest import Client

from .models import Call
from .serializers import CallSerializer
from ..activity.models import Activity


logger = logging.getLogger(__name__)


MODULE_MAP = {
    "lead": ("leads", "lead"),
    "company": ("companies", "company"),
    "deal": ("deals", "deal"),
    "ticket": ("tickets", "ticket"),
}


# ============================================================
# TWILIO STATUS -> CRM OUTCOME
# ============================================================

def get_call_outcome(twilio_status):
    status_map = {
        "completed": "connected",
        "no-answer": "no_answer",
        "busy": "busy",
        "failed": "other",
        "canceled": "other",
    }

    return status_map.get(twilio_status)


# ============================================================
# TERMINAL TWILIO STATUSES
# ============================================================

TERMINAL_STATUSES = {
    "completed",
    "busy",
    "no-answer",
    "failed",
    "canceled",
}


# ============================================================
# GET ALL CALLS / CREATE CALL
# ============================================================

class CallListCreateView(generics.ListCreateAPIView):

    queryset = Call.objects.all().select_related(
        "activity",
        "activity__created_by",
        "connected_content_type",
    )

    serializer_class = CallSerializer


# ============================================================
# CALL DETAIL
# ============================================================

class CallDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Call.objects.all().select_related(
        "activity",
        "activity__created_by",
        "connected_content_type",
    )

    serializer_class = CallSerializer


# ============================================================
# START TWILIO TRIAL CALL
# ============================================================

class StartCallView(APIView):

    def post(self, request):

        print("\n================================")
        print("START TWILIO TRIAL CALL")
        print("================================")

        module = request.data.get("module")
        module_id = request.data.get("module_id")

        print("Module:", module)
        print("Module ID:", module_id)

        # --------------------------------------------------------
        # VALIDATE MODULE
        # --------------------------------------------------------

        if not module:
            return Response(
                {"detail": "module is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not module_id:
            return Response(
                {"detail": "module_id is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        module = str(module).strip().lower()

        if module not in MODULE_MAP:
            return Response(
                {
                    "detail": f"Unsupported module: {module}"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # --------------------------------------------------------
        # GET CONTENT TYPE
        # --------------------------------------------------------

        app_label, model_name = MODULE_MAP[module]

        try:
            content_type = ContentType.objects.get(
                app_label=app_label,
                model=model_name,
            )

        except ContentType.DoesNotExist:

            return Response(
                {
                    "detail": "Module configuration not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        # --------------------------------------------------------
        # GET MODEL
        # --------------------------------------------------------

        model_class = content_type.model_class()

        if not model_class:

            return Response(
                {
                    "detail": (
                        f"Model for '{module}' "
                        "could not be found."
                    )
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        # --------------------------------------------------------
        # GET CRM OBJECT
        # --------------------------------------------------------

        try:

            obj = model_class.objects.get(
                pk=module_id
            )

        except model_class.DoesNotExist:

            return Response(
                {
                    "detail": (
                        f"{module.title()} "
                        f"with ID {module_id} does not exist."
                    )
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        # --------------------------------------------------------
        # FIND CUSTOMER PHONE
        # --------------------------------------------------------

        customer_phone = None

        possible_phone_fields = [
            "phone_number",
            "phone",
            "mobile_number",
            "mobile",
        ]

        for field in possible_phone_fields:

            value = getattr(
                obj,
                field,
                None,
            )

            if value:

                customer_phone = str(
                    value
                ).strip()

                break

        print(
            "Customer phone:",
            customer_phone,
        )

        if not customer_phone:

            return Response(
                {
                    "detail": (
                        f"No phone number found "
                        f"for this {module}."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # --------------------------------------------------------
        # AUTHENTICATION
        # --------------------------------------------------------

        user = request.user

        if not user or not user.is_authenticated:

            return Response(
                {
                    "detail": "Authentication required."
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # --------------------------------------------------------
        # TWILIO SETTINGS
        # --------------------------------------------------------

        account_sid = getattr(
            settings,
            "TWILIO_ACCOUNT_SID",
            None,
        )

        auth_token = getattr(
            settings,
            "TWILIO_AUTH_TOKEN",
            None,
        )

        twilio_phone = getattr(
            settings,
            "TWILIO_PHONE_NUMBER",
            None,
        )

        if not account_sid:

            return Response(
                {
                    "detail": (
                        "TWILIO_ACCOUNT_SID "
                        "is not configured."
                    )
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        if not auth_token:

            return Response(
                {
                    "detail": (
                        "TWILIO_AUTH_TOKEN "
                        "is not configured."
                    )
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        if not twilio_phone:

            return Response(
                {
                    "detail": (
                        "TWILIO_PHONE_NUMBER "
                        "is not configured."
                    )
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # --------------------------------------------------------
        # CREATE TWILIO CLIENT
        # --------------------------------------------------------

        client = Client(
            account_sid,
            auth_token,
        )

        # --------------------------------------------------------
        # TWILIO TRIAL TEMPLATE
        # --------------------------------------------------------

        trial_webhook_url = (
            "https://webhooks.twilio.com/v1/Voice/Template/"
            "voice_text_to_speech"
        )

        print(
            "Twilio Trial Template:",
            trial_webhook_url,
        )

        # --------------------------------------------------------
        # CREATE TWILIO CALL
        # --------------------------------------------------------

        try:

            twilio_call = client.calls.create(
                to=customer_phone,
                from_=twilio_phone,
                url=trial_webhook_url,
            )

        except Exception as exc:

            logger.exception(
                "Twilio Trial call failed"
            )

            print("\n================================")
            print("TWILIO CALL ERROR")
            print("================================")
            print(exc)

            return Response(
                {
                    "detail": (
                        "Twilio call could not "
                        "be created."
                    ),
                    "error": str(exc),
                },
                status=status.HTTP_502_BAD_GATEWAY,
            )

        print("\n================================")
        print("TWILIO CALL CREATED")
        print("================================")

        print(
            "Call SID:",
            twilio_call.sid,
        )

        print(
            "Status:",
            twilio_call.status,
        )

        print(
            "To:",
            customer_phone,
        )

        print(
            "From:",
            twilio_phone,
        )

        # --------------------------------------------------------
        # SAVE CRM CALL
        # --------------------------------------------------------

        try:

            with transaction.atomic():

                activity = Activity.objects.create(
                    activity_type="call",
                    created_by=user,
                    content_type=content_type,
                    object_id=module_id,
                )

                crm_call = Call.objects.create(
                    activity=activity,

                    connected_content_type=content_type,

                    connected_object_id=module_id,

                    twilio_call_sid=twilio_call.sid,

                    twilio_status=twilio_call.status,

                    call_outcome="other",

                    duration=None,

                    date=activity.created_at.date(),

                    time=activity.created_at.time(),

                    note="",
                )

        except Exception as exc:

            logger.exception(
                "CRM Call record creation failed"
            )

            return Response(
                {
                    "detail": (
                        "Twilio call was created, "
                        "but CRM Call record "
                        "could not be saved."
                    ),
                    "call_sid": twilio_call.sid,
                    "error": str(exc),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        print("\n================================")
        print("CRM CALL SAVED")
        print("================================")

        print(
            "CRM Call ID:",
            crm_call.id,
        )

        print(
            "Twilio Call SID:",
            crm_call.twilio_call_sid,
        )

        print(
            "Twilio Status:",
            crm_call.twilio_status,
        )

        # --------------------------------------------------------
        # RESPONSE
        # --------------------------------------------------------

        return Response(
            {
                "message": (
                    "Twilio Trial call started "
                    "and CRM Call saved."
                ),

                "id": crm_call.id,

                "call_sid": (
                    crm_call.twilio_call_sid
                ),

                "status": (
                    crm_call.twilio_status
                ),

                "to": customer_phone,

                "from": twilio_phone,

                "module": module,

                "module_id": module_id,
            },
            status=status.HTTP_201_CREATED,
        )


# ============================================================
# SYNC CALL STATUS FROM TWILIO
# ============================================================

class SyncCallView(APIView):

    def get(self, request, pk):

        print("\n================================")
        print("SYNC TWILIO CALL")
        print("================================")

        # --------------------------------------------------------
        # GET CRM CALL
        # --------------------------------------------------------

        try:

            crm_call = Call.objects.select_related(
                "activity",
                "activity__created_by",
                "connected_content_type",
            ).get(pk=pk)

        except Call.DoesNotExist:

            return Response(
                {
                    "detail": "Call not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        # --------------------------------------------------------
        # CHECK TWILIO SID
        # --------------------------------------------------------

        if not crm_call.twilio_call_sid:

            return Response(
                {
                    "detail": (
                        "This CRM call does not "
                        "have a Twilio Call SID."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # --------------------------------------------------------
        # TWILIO SETTINGS
        # --------------------------------------------------------

        account_sid = getattr(
            settings,
            "TWILIO_ACCOUNT_SID",
            None,
        )

        auth_token = getattr(
            settings,
            "TWILIO_AUTH_TOKEN",
            None,
        )

        if not account_sid or not auth_token:

            return Response(
                {
                    "detail": (
                        "Twilio credentials "
                        "are not configured."
                    )
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # --------------------------------------------------------
        # FETCH TWILIO CALL
        # --------------------------------------------------------

        try:

            client = Client(
                account_sid,
                auth_token,
            )

            twilio_call = client.calls(
                crm_call.twilio_call_sid
            ).fetch()

        except Exception as exc:

            logger.exception(
                "Could not fetch Twilio call"
            )

            return Response(
                {
                    "detail": (
                        "Could not fetch "
                        "Twilio call."
                    ),
                    "error": str(exc),
                },
                status=status.HTTP_502_BAD_GATEWAY,
            )

        # --------------------------------------------------------
        # GET STATUS
        # --------------------------------------------------------

        twilio_status = (
            twilio_call.status
        )

        # --------------------------------------------------------
        # GET DURATION
        # --------------------------------------------------------

        duration = None

        if twilio_call.duration:

            try:

                duration = int(
                    twilio_call.duration
                )

            except (
                TypeError,
                ValueError,
            ):

                duration = None

        # --------------------------------------------------------
        # UPDATE CRM CALL
        # --------------------------------------------------------

        crm_call.twilio_status = twilio_status

        # Duration is only reliable once Twilio
        # has a value.

        if duration is not None:

            crm_call.duration = duration

        # --------------------------------------------------------
        # UPDATE OUTCOME ONLY WHEN TERMINAL
        # --------------------------------------------------------

        outcome = get_call_outcome(
            twilio_status
        )

        if outcome:

            crm_call.call_outcome = outcome

        crm_call.save(
            update_fields=[
                "twilio_status",
                "duration",
                "call_outcome",
                "updated_at",
            ]
        )

        # --------------------------------------------------------
        # SERIALIZE UPDATED CALL
        # --------------------------------------------------------

        serializer = CallSerializer(
            crm_call,
            context={
                "request": request,
            },
        )

        print(
            "Twilio Status:",
            twilio_status,
        )

        print(
            "Duration:",
            duration,
        )

        print(
            "Outcome:",
            crm_call.call_outcome,
        )

        print("\n================================")
        print("CALL SYNC COMPLETE")
        print("================================")

        return Response(
            {
                "call": serializer.data,

                "twilio_status": twilio_status,

                "duration": duration,

                "call_outcome": (
                    crm_call.call_outcome
                ),

                "is_terminal": (
                    twilio_status
                    in TERMINAL_STATUSES
                ),
            },
            status=status.HTTP_200_OK,
        )