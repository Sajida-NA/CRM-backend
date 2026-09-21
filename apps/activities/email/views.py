# # from rest_framework.views import APIView
# # from rest_framework.response import Response
# # from rest_framework import status
# # from rest_framework.permissions import IsAuthenticated

# # from django.contrib.contenttypes.models import ContentType
# # from django.core.mail import EmailMessage
# # from django.conf import settings
# # from django.utils import timezone
# # from django.contrib.auth import get_user_model

# # from .models import Email
# # from .serializers import EmailSerializer

# # from apps.activities.activity.models import Activity
# # from apps.leads.models import Lead
# # from apps.deals.models import Deal
# # from apps.companies.models import Company
# # from apps.tickets.models import Ticket

# # from apps.notifications.models import Notification


# # User = get_user_model()


# # # =====================================================
# # # GET RECIPIENT DETAILS
# # # =====================================================

# # def get_recipient_details(module, object_id):

# #     module = module.lower().strip()

# #     # =================================================
# #     # LEAD
# #     # =================================================

# #     if module == "lead":

# #         lead = Lead.objects.get(pk=object_id)

# #         return {
# #             "id": lead.id,
# #             "name": (
# #                 f"{lead.first_name} {lead.last_name}"
# #             ).strip(),
# #             "email": lead.email,
# #         }

# #     # =================================================
# #     # COMPANY
# #     # =================================================

# #     elif module == "company":

# #         company = Company.objects.get(pk=object_id)

# #         return {
# #             "id": company.id,
# #             "name": getattr(
# #                 company,
# #                 "company_name",
# #                 None
# #             ),
# #             "email": getattr(
# #                 company,
# #                 "email",
# #                 None
# #             ),
# #         }

# #     # =================================================
# #     # DEAL
# #     # =================================================

# #     elif module == "deal":

# #         deal = Deal.objects.select_related(
# #             "associated_lead"
# #         ).get(pk=object_id)

# #         lead = deal.associated_lead

# #         if not lead:
# #             return {
# #                 "id": deal.id,
# #                 "name": None,
# #                 "email": None,
# #             }

# #         return {
# #             "id": deal.id,
# #             "name": (
# #                 f"{lead.first_name} {lead.last_name}"
# #             ).strip(),
# #             "email": lead.email,
# #         }

# #     # =================================================
# #     # TICKET
# #     # =================================================

# #     elif module == "ticket":

# #         ticket = Ticket.objects.select_related(
# #             "associated_deal__associated_lead"
# #         ).get(pk=object_id)

# #         deal = ticket.associated_deal

# #         if not deal:
# #             return {
# #                 "id": ticket.id,
# #                 "name": None,
# #                 "email": None,
# #             }

# #         lead = deal.associated_lead

# #         if not lead:
# #             return {
# #                 "id": ticket.id,
# #                 "name": None,
# #                 "email": None,
# #             }

# #         return {
# #             "id": ticket.id,
# #             "name": (
# #                 f"{lead.first_name} {lead.last_name}"
# #             ).strip(),
# #             "email": lead.email,
# #         }

# #     raise ValueError("Invalid module")


# # # =====================================================
# # # EMAIL LIST + CREATE
# # # =====================================================

# # class EmailListCreateView(APIView):

# #     permission_classes = [IsAuthenticated]

# #     # =================================================
# #     # GET
# #     # =================================================

# #     def get(self, request):

# #         emails = Email.objects.select_related(
# #             "activity",
# #             "activity__created_by"
# #         ).order_by(
# #             "-activity__created_at"
# #         )

# #         serializer = EmailSerializer(
# #             emails,
# #             many=True
# #         )

# #         return Response(
# #             serializer.data,
# #             status=status.HTTP_200_OK
# #         )

# #     # =================================================
# #     # POST
# #     # =================================================

# #     def post(self, request):

# #         # ---------------------------------------------
# #         # Get request data
# #         # ---------------------------------------------

# #         sender_id = request.data.get("sender_id")
# #         module = request.data.get("module")
# #         recipient_id = request.data.get("recipient_id")

# #         # ---------------------------------------------
# #         # Validate sender
# #         # ---------------------------------------------

# #         if not sender_id:

# #             return Response(
# #                 {
# #                     "error": "sender_id is required."
# #                 },
# #                 status=status.HTTP_400_BAD_REQUEST
# #             )

# #         try:

# #             sender = User.objects.get(
# #                 pk=sender_id
# #             )

# #         except User.DoesNotExist:

# #             return Response(
# #                 {
# #                     "error": (
# #                         f"User with id "
# #                         f"{sender_id} not found."
# #                     )
# #                 },
# #                 status=status.HTTP_404_NOT_FOUND
# #             )

# #         # ---------------------------------------------
# #         # Validate module
# #         # ---------------------------------------------

# #         if not module:

# #             return Response(
# #                 {
# #                     "error": "module is required."
# #                 },
# #                 status=status.HTTP_400_BAD_REQUEST
# #             )

# #         module = module.lower().strip()

# #         allowed_modules = [
# #             "lead",
# #             "deal",
# #             "company",
# #             "ticket",
# #         ]

# #         if module not in allowed_modules:

# #             return Response(
# #                 {
# #                     "error": (
# #                         "module must be 'lead', 'deal', "
# #                         "'company', or 'ticket'."
# #                     )
# #                 },
# #                 status=status.HTTP_400_BAD_REQUEST
# #             )

# #         # ---------------------------------------------
# #         # Validate recipient ID
# #         # ---------------------------------------------

# #         if not recipient_id:

# #             return Response(
# #                 {
# #                     "error": "recipient_id is required."
# #                 },
# #                 status=status.HTTP_400_BAD_REQUEST
# #             )

# #         # ---------------------------------------------
# #         # Select CRM model
# #         # ---------------------------------------------

# #         if module == "lead":

# #             model = Lead

# #         elif module == "deal":

# #             model = Deal

# #         elif module == "company":

# #             model = Company

# #         elif module == "ticket":

# #             model = Ticket

# #         # ---------------------------------------------
# #         # Get related CRM object
# #         # ---------------------------------------------

# #         try:

# #             related_object = model.objects.get(
# #                 pk=recipient_id
# #             )

# #         except model.DoesNotExist:

# #             return Response(
# #                 {
# #                     "error": (
# #                         f"{module} with id "
# #                         f"{recipient_id} not found."
# #                     )
# #                 },
# #                 status=status.HTTP_404_NOT_FOUND
# #             )

# #         # ---------------------------------------------
# #         # Get recipient name + email
# #         # ---------------------------------------------

# #         recipient_name = None
# #         recipient_email = None

# #         # =================================================
# #         # LEAD
# #         # =================================================

# #         if module == "lead":

# #             recipient_name = (
# #                 f"{related_object.first_name} "
# #                 f"{related_object.last_name}"
# #             ).strip()

# #             recipient_email = related_object.email

# #         # =================================================
# #         # DEAL
# #         # =================================================

# #         elif module == "deal":

# #             lead = related_object.associated_lead

# #             if lead:

# #                 recipient_name = (
# #                     f"{lead.first_name} "
# #                     f"{lead.last_name}"
# #                 ).strip()

# #                 recipient_email = lead.email

# #         # =================================================
# #         # COMPANY
# #         # =================================================

# #         elif module == "company":

# #             recipient_name = getattr(
# #                 related_object,
# #                 "company_name",
# #                 None
# #             )

# #             recipient_email = getattr(
# #                 related_object,
# #                 "email",
# #                 None
# #             )

# #         # =================================================
# #         # TICKET
# #         # =================================================
# #         #
# #         # IMPORTANT:
# #         # Ticket customer comes from:
# #         #
# #         # Ticket
# #         #   -> associated_deal
# #         #       -> associated_lead
# #         #           -> email
# #         #
# #         # Do NOT use ticket_owner here.
# #         # =================================================

# #         elif module == "ticket":

# #             deal = related_object.associated_deal

# #             if deal:

# #                 lead = deal.associated_lead

# #                 if lead:

# #                     recipient_name = (
# #                         f"{lead.first_name} "
# #                         f"{lead.last_name}"
# #                     ).strip()

# #                     recipient_email = lead.email

# #         # ---------------------------------------------
# #         # Validate recipient email
# #         # ---------------------------------------------

# #         if not recipient_email:

# #             return Response(
# #                 {
# #                     "error": (
# #                         f"{module} with id "
# #                         f"{recipient_id} does not have "
# #                         f"a recipient email."
# #                     )
# #                 },
# #                 status=status.HTTP_400_BAD_REQUEST
# #             )

# #         # ---------------------------------------------
# #         # Email fields
# #         # ---------------------------------------------

# #         subject = request.data.get(
# #             "subject",
# #             ""
# #         )

# #         body = request.data.get(
# #             "body",
# #             ""
# #         )

# #         cc = request.data.get(
# #             "cc",
# #             []
# #         )

# #         bcc = request.data.get(
# #             "bcc",
# #             []
# #         )

# #         if not isinstance(cc, list):

# #             return Response(
# #                 {
# #                     "error": "cc must be a list."
# #                 },
# #                 status=status.HTTP_400_BAD_REQUEST
# #             )

# #         if not isinstance(bcc, list):

# #             return Response(
# #                 {
# #                     "error": "bcc must be a list."
# #                 },
# #                 status=status.HTTP_400_BAD_REQUEST
# #             )

# #         # ---------------------------------------------
# #         # ContentType
# #         # ---------------------------------------------

# #         content_type = ContentType.objects.get_for_model(
# #             model
# #         )

# #         # ---------------------------------------------
# #         # Create Activity
# #         # ---------------------------------------------

# #         activity = Activity.objects.create(
# #             activity_type="email",
# #             created_by=sender,
# #             content_type=content_type,
# #             object_id=related_object.pk
# #         )

# #         # ---------------------------------------------
# #         # Recipient JSON
# #         # ---------------------------------------------

# #         to_recipients = [
# #             {
# #                 "id": related_object.pk,
# #                 "name": recipient_name,
# #                 "email": recipient_email,
# #             }
# #         ]

# #         # ---------------------------------------------
# #         # Convert CC
# #         # ---------------------------------------------

# #         cc_emails = []

# #         for recipient in cc:

# #             if isinstance(recipient, dict):

# #                 email_address = recipient.get(
# #                     "email"
# #                 )

# #                 if email_address:
# #                     cc_emails.append(
# #                         email_address
# #                     )

# #             elif isinstance(recipient, str):

# #                 if recipient.strip():
# #                     cc_emails.append(
# #                         recipient.strip()
# #                     )

# #         # ---------------------------------------------
# #         # Convert BCC
# #         # ---------------------------------------------

# #         bcc_emails = []

# #         for recipient in bcc:

# #             if isinstance(recipient, dict):

# #                 email_address = recipient.get(
# #                     "email"
# #                 )

# #                 if email_address:
# #                     bcc_emails.append(
# #                         email_address
# #                     )

# #             elif isinstance(recipient, str):

# #                 if recipient.strip():
# #                     bcc_emails.append(
# #                         recipient.strip()
# #                     )

# #         # ---------------------------------------------
# #         # Create Email
# #         # ---------------------------------------------

# #         email = Email.objects.create(
# #             activity=activity,
# #             to_recipients=to_recipients,
# #             cc=cc,
# #             bcc=bcc,
# #             subject=subject,
# #             body=body,
# #             status="draft"
# #         )

# #         # ---------------------------------------------
# #         # Send Email
# #         # ---------------------------------------------

# #         try:

# #             email_message = EmailMessage(
# #                 subject=subject,
# #                 body=body,
# #                 from_email=settings.DEFAULT_FROM_EMAIL,
# #                 to=[recipient_email],
# #                 cc=cc_emails,
# #                 bcc=bcc_emails
# #             )

# #             email_message.send(
# #                 fail_silently=False
# #             )

# #             # -----------------------------------------
# #             # Success
# #             # -----------------------------------------

# #             email.status = "sent"

# #             email.sent_at = timezone.now()

# #             email.error_message = None

# #             email.save(
# #                 update_fields=[
# #                     "status",
# #                     "sent_at",
# #                     "error_message"
# #                 ]
# #             )

# #             Notification.objects.create(
# #                 user=request.user,
# #                 title="Email Sent",
# #                 message=(
# #                     f"Email '{email.subject}' "
# #                     f"has been sent successfully."
# #                 ),
# #             )

# #         except Exception as e:

# #             # -----------------------------------------
# #             # Failed
# #             # -----------------------------------------

# #             email.status = "failed"

# #             email.error_message = str(e)

# #             email.sent_at = None

# #             email.save(
# #                 update_fields=[
# #                     "status",
# #                     "error_message",
# #                     "sent_at"
# #                 ]
# #             )

# #             Notification.objects.create(
# #                 user=request.user,
# #                 title="Email Failed",
# #                 message=(
# #                     f"Email '{email.subject}' "
# #                     f"failed to send."
# #                 ),
# #             )

# #         # ---------------------------------------------
# #         # Response
# #         # ---------------------------------------------

# #         response_serializer = EmailSerializer(
# #             email
# #         )

# #         return Response(
# #             response_serializer.data,
# #             status=status.HTTP_201_CREATED
# #         )


# # # =====================================================
# # # EMAIL DETAIL
# # # =====================================================

# # class EmailDetailView(APIView):

# #     permission_classes = [IsAuthenticated]

# #     def get_object(self, pk):

# #         try:

# #             return Email.objects.select_related(
# #                 "activity",
# #                 "activity__created_by"
# #             ).get(
# #                 pk=pk
# #             )

# #         except Email.DoesNotExist:

# #             return None

# #     # =================================================
# #     # GET
# #     # =================================================

# #     def get(self, request, pk):

# #         email = self.get_object(pk)

# #         if email is None:

# #             return Response(
# #                 {
# #                     "detail": "Email not found."
# #                 },
# #                 status=status.HTTP_404_NOT_FOUND
# #             )

# #         serializer = EmailSerializer(
# #             email
# #         )

# #         return Response(
# #             serializer.data,
# #             status=status.HTTP_200_OK
# #         )

# #     # =================================================
# #     # PUT
# #     # =================================================

# #     def put(self, request, pk):

# #         email = self.get_object(pk)

# #         if email is None:

# #             return Response(
# #                 {
# #                     "detail": "Email not found."
# #                 },
# #                 status=status.HTTP_404_NOT_FOUND
# #             )

# #         serializer = EmailSerializer(
# #             email,
# #             data=request.data,
# #             partial=True
# #         )

# #         if serializer.is_valid():

# #             serializer.save()

# #             Notification.objects.create(
# #                 user=request.user,
# #                 title="Email Updated",
# #                 message=(
# #                     f"Email '{email.subject}' "
# #                     f"has been updated."
# #                 ),
# #             )

# #             return Response(
# #                 EmailSerializer(email).data,
# #                 status=status.HTTP_200_OK
# #             )

# #         return Response(
# #             serializer.errors,
# #             status=status.HTTP_400_BAD_REQUEST
# #         )

# #     # =================================================
# #     # DELETE
# #     # =================================================

# #     def delete(self, request, pk):

# #         email = self.get_object(pk)

# #         if email is None:

# #             return Response(
# #                 {
# #                     "detail": "Email not found."
# #                 },
# #                 status=status.HTTP_404_NOT_FOUND
# #             )

# #         email_subject = email.subject

# #         email.delete()

# #         Notification.objects.create(
# #             user=request.user,
# #             title="Email Deleted",
# #             message=(
# #                 f"Email '{email_subject}' "
# #                 f"has been deleted."
# #             ),
# #         )

# #         return Response(
# #             {
# #                 "message": "Email deleted successfully."
# #             },
# #             status=status.HTTP_204_NO_CONTENT
# #         )


# # # =====================================================
# # # EMAIL RECIPIENT
# # # =====================================================

# # class EmailRecipientView(APIView):

# #     permission_classes = [IsAuthenticated]

# #     def get(self, request, module, object_id):

# #         module = module.lower().strip()

# #         allowed_modules = [
# #             "lead",
# #             "deal",
# #             "company",
# #             "ticket",
# #         ]

# #         if module not in allowed_modules:

# #             return Response(
# #                 {
# #                     "error": "Invalid module."
# #                 },
# #                 status=status.HTTP_400_BAD_REQUEST
# #             )

# #         try:

# #             recipient = get_recipient_details(
# #                 module,
# #                 object_id
# #             )

# #             if not recipient.get("email"):

# #                 return Response(
# #                     {
# #                         "error": (
# #                             f"{module} with id "
# #                             f"{object_id} does not have "
# #                             f"a recipient email."
# #                         )
# #                     },
# #                     status=status.HTTP_400_BAD_REQUEST
# #                 )

# #             return Response(
# #                 recipient,
# #                 status=status.HTTP_200_OK
# #             )

# #         except (
# #             Lead.DoesNotExist,
# #             Company.DoesNotExist,
# #             Deal.DoesNotExist,
# #             Ticket.DoesNotExist,
# #         ):

# #             return Response(
# #                 {
# #                     "error": (
# #                         f"{module} with id "
# #                         f"{object_id} not found."
# #                     )
# #                 },
# #                 status=status.HTTP_404_NOT_FOUND
# #             )

# #         except ValueError as error:

# #             return Response(
# #                 {
# #                     "error": str(error)
# #                 },
# #                 status=status.HTTP_400_BAD_REQUEST
# #             )



# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated

# from django.contrib.contenttypes.models import ContentType
# from django.core.mail import EmailMessage
# from django.conf import settings
# from django.utils import timezone
# from django.contrib.auth import get_user_model

# import traceback

# from .models import Email
# from .serializers import EmailSerializer

# from apps.activities.activity.models import Activity
# from apps.leads.models import Lead
# from apps.deals.models import Deal
# from apps.companies.models import Company
# from apps.tickets.models import Ticket

# from apps.notifications.models import Notification


# User = get_user_model()


# # =====================================================
# # GET RECIPIENT DETAILS
# # =====================================================

# def get_recipient_details(module, object_id):

#     module = module.lower().strip()

#     # =================================================
#     # LEAD
#     # =================================================

#     if module == "lead":

#         lead = Lead.objects.get(pk=object_id)

#         return {
#             "id": lead.id,
#             "name": (
#                 f"{lead.first_name} {lead.last_name}"
#             ).strip(),
#             "email": lead.email,
#         }

#     # =================================================
#     # COMPANY
#     # =================================================

#     elif module == "company":

#         company = Company.objects.get(pk=object_id)

#         return {
#             "id": company.id,
#             "name": getattr(
#                 company,
#                 "company_name",
#                 None
#             ),
#             "email": getattr(
#                 company,
#                 "email",
#                 None
#             ),
#         }

#     # =================================================
#     # DEAL
#     # =================================================

#     elif module == "deal":

#         deal = Deal.objects.select_related(
#             "associated_lead"
#         ).get(pk=object_id)

#         lead = deal.associated_lead

#         if not lead:
#             return {
#                 "id": deal.id,
#                 "name": None,
#                 "email": None,
#             }

#         return {
#             "id": deal.id,
#             "name": (
#                 f"{lead.first_name} {lead.last_name}"
#             ).strip(),
#             "email": lead.email,
#         }

#     # =================================================
#     # TICKET
#     # =================================================

#     elif module == "ticket":

#         ticket = Ticket.objects.select_related(
#             "associated_deal__associated_lead"
#         ).get(pk=object_id)

#         deal = ticket.associated_deal

#         if not deal:
#             return {
#                 "id": ticket.id,
#                 "name": None,
#                 "email": None,
#             }

#         lead = deal.associated_lead

#         if not lead:
#             return {
#                 "id": ticket.id,
#                 "name": None,
#                 "email": None,
#             }

#         return {
#             "id": ticket.id,
#             "name": (
#                 f"{lead.first_name} {lead.last_name}"
#             ).strip(),
#             "email": lead.email,
#         }

#     raise ValueError("Invalid module")


# # =====================================================
# # EMAIL LIST + CREATE
# # =====================================================

# class EmailListCreateView(APIView):

#     permission_classes = [IsAuthenticated]

#     # =================================================
#     # GET
#     # =================================================

#     def get(self, request):

#         emails = Email.objects.select_related(
#             "activity",
#             "activity__created_by"
#         ).order_by(
#             "-activity__created_at"
#         )

#         serializer = EmailSerializer(
#             emails,
#             many=True
#         )

#         return Response(
#             serializer.data,
#             status=status.HTTP_200_OK
#         )

#     # =================================================
#     # POST
#     # =================================================

#     def post(self, request):

#         # ---------------------------------------------
#         # Get request data
#         # ---------------------------------------------

#         sender_id = request.data.get("sender_id")
#         module = request.data.get("module")
#         recipient_id = request.data.get("recipient_id")

#         print("========== EMAIL REQUEST ==========")
#         print("Sender ID:", sender_id)
#         print("Module:", module)
#         print("Recipient ID:", recipient_id)
#         print("===================================")

#         # ---------------------------------------------
#         # Validate sender
#         # ---------------------------------------------

#         if not sender_id:

#             return Response(
#                 {
#                     "error": "sender_id is required."
#                 },
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         try:

#             sender = User.objects.get(
#                 pk=sender_id
#             )

#         except User.DoesNotExist:

#             return Response(
#                 {
#                     "error": (
#                         f"User with id "
#                         f"{sender_id} not found."
#                     )
#                 },
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         # ---------------------------------------------
#         # Validate module
#         # ---------------------------------------------

#         if not module:

#             return Response(
#                 {
#                     "error": "module is required."
#                 },
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         module = module.lower().strip()

#         allowed_modules = [
#             "lead",
#             "deal",
#             "company",
#             "ticket",
#         ]

#         if module not in allowed_modules:

#             return Response(
#                 {
#                     "error": (
#                         "module must be 'lead', 'deal', "
#                         "'company', or 'ticket'."
#                     )
#                 },
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # ---------------------------------------------
#         # Validate recipient ID
#         # ---------------------------------------------

#         if not recipient_id:

#             return Response(
#                 {
#                     "error": "recipient_id is required."
#                 },
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # ---------------------------------------------
#         # Select CRM model
#         # ---------------------------------------------

#         if module == "lead":

#             model = Lead

#         elif module == "deal":

#             model = Deal

#         elif module == "company":

#             model = Company

#         elif module == "ticket":

#             model = Ticket

#         # ---------------------------------------------
#         # Get related CRM object
#         # ---------------------------------------------

#         try:

#             related_object = model.objects.get(
#                 pk=recipient_id
#             )

#         except model.DoesNotExist:

#             return Response(
#                 {
#                     "error": (
#                         f"{module} with id "
#                         f"{recipient_id} not found."
#                     )
#                 },
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         # ---------------------------------------------
#         # Get recipient name + email
#         # ---------------------------------------------

#         recipient_name = None
#         recipient_email = None

#         # =================================================
#         # LEAD
#         # =================================================

#         if module == "lead":

#             recipient_name = (
#                 f"{related_object.first_name} "
#                 f"{related_object.last_name}"
#             ).strip()

#             recipient_email = related_object.email

#         # =================================================
#         # DEAL
#         # =================================================

#         elif module == "deal":

#             lead = related_object.associated_lead

#             if lead:

#                 recipient_name = (
#                     f"{lead.first_name} "
#                     f"{lead.last_name}"
#                 ).strip()

#                 recipient_email = lead.email

#         # =================================================
#         # COMPANY
#         # =================================================

#         elif module == "company":

#             recipient_name = getattr(
#                 related_object,
#                 "company_name",
#                 None
#             )

#             recipient_email = getattr(
#                 related_object,
#                 "email",
#                 None
#             )

#         # =================================================
#         # TICKET
#         # =================================================

#         elif module == "ticket":

#             deal = related_object.associated_deal

#             if deal:

#                 lead = deal.associated_lead

#                 if lead:

#                     recipient_name = (
#                         f"{lead.first_name} "
#                         f"{lead.last_name}"
#                     ).strip()

#                     recipient_email = lead.email

#         # ---------------------------------------------
#         # Validate recipient email
#         # ---------------------------------------------

#         print("Recipient Name:", recipient_name)
#         print("Recipient Email:", recipient_email)

#         if not recipient_email:

#             return Response(
#                 {
#                     "error": (
#                         f"{module} with id "
#                         f"{recipient_id} does not have "
#                         f"a recipient email."
#                     )
#                 },
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # ---------------------------------------------
#         # Email fields
#         # ---------------------------------------------

#         subject = request.data.get(
#             "subject",
#             ""
#         )

#         body = request.data.get(
#             "body",
#             ""
#         )

#         cc = request.data.get(
#             "cc",
#             []
#         )

#         bcc = request.data.get(
#             "bcc",
#             []
#         )

#         if not isinstance(cc, list):

#             return Response(
#                 {
#                     "error": "cc must be a list."
#                 },
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         if not isinstance(bcc, list):

#             return Response(
#                 {
#                     "error": "bcc must be a list."
#                 },
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # ---------------------------------------------
#         # ContentType
#         # ---------------------------------------------

#         content_type = ContentType.objects.get_for_model(
#             model
#         )

#         # ---------------------------------------------
#         # Create Activity
#         # ---------------------------------------------

#         activity = Activity.objects.create(
#             activity_type="email",
#             created_by=sender,
#             content_type=content_type,
#             object_id=related_object.pk
#         )

#         # ---------------------------------------------
#         # Recipient JSON
#         # ---------------------------------------------

#         to_recipients = [
#             {
#                 "id": related_object.pk,
#                 "name": recipient_name,
#                 "email": recipient_email,
#             }
#         ]

#         # ---------------------------------------------
#         # Convert CC
#         # ---------------------------------------------

#         cc_emails = []

#         for recipient in cc:

#             if isinstance(recipient, dict):

#                 email_address = recipient.get(
#                     "email"
#                 )

#                 if email_address:

#                     cc_emails.append(
#                         email_address
#                     )

#             elif isinstance(recipient, str):

#                 if recipient.strip():

#                     cc_emails.append(
#                         recipient.strip()
#                     )

#         # ---------------------------------------------
#         # Convert BCC
#         # ---------------------------------------------

#         bcc_emails = []

#         for recipient in bcc:

#             if isinstance(recipient, dict):

#                 email_address = recipient.get(
#                     "email"
#                 )

#                 if email_address:

#                     bcc_emails.append(
#                         email_address
#                     )

#             elif isinstance(recipient, str):

#                 if recipient.strip():

#                     bcc_emails.append(
#                         recipient.strip()
#                     )

#         # ---------------------------------------------
#         # Create Email
#         # ---------------------------------------------

#         email = Email.objects.create(
#             activity=activity,
#             to_recipients=to_recipients,
#             cc=cc,
#             bcc=bcc,
#             subject=subject,
#             body=body,
#             status="draft"
#         )

#         # ---------------------------------------------
#         # Send Email
#         # ---------------------------------------------

#         try:

#             print("========== SMTP DEBUG ==========")
#             print(
#                 "EMAIL_HOST:",
#                 getattr(
#                     settings,
#                     "EMAIL_HOST",
#                     None
#                 )
#             )
#             print(
#                 "EMAIL_PORT:",
#                 getattr(
#                     settings,
#                     "EMAIL_PORT",
#                     None
#                 )
#             )
#             print(
#                 "EMAIL_USE_TLS:",
#                 getattr(
#                     settings,
#                     "EMAIL_USE_TLS",
#                     None
#                 )
#             )
#             print(
#                 "EMAIL_HOST_USER:",
#                 getattr(
#                     settings,
#                     "EMAIL_HOST_USER",
#                     None
#                 )
#             )
#             print(
#                 "DEFAULT_FROM_EMAIL:",
#                 getattr(
#                     settings,
#                     "DEFAULT_FROM_EMAIL",
#                     None
#                 )
#             )
#             print(
#                 "TO:",
#                 recipient_email
#             )
#             print("================================")

#             email_message = EmailMessage(
#                 subject=subject,
#                 body=body,
#                 from_email=settings.DEFAULT_FROM_EMAIL,
#                 to=[recipient_email],
#                 cc=cc_emails,
#                 bcc=bcc_emails
#             )

#             print("Creating EmailMessage: SUCCESS")
#             print("Trying to send email...")

#             email_message.send(
#                 fail_silently=False
#             )

#             print("Email sent successfully.")

#             # -----------------------------------------
#             # Success
#             # -----------------------------------------

#             email.status = "sent"

#             email.sent_at = timezone.now()

#             email.error_message = None

#             email.save(
#                 update_fields=[
#                     "status",
#                     "sent_at",
#                     "error_message"
#                 ]
#             )

#             Notification.objects.create(
#                 user=request.user,
#                 title="Email Sent",
#                 message=(
#                     f"Email '{email.subject}' "
#                     f"has been sent successfully."
#                 ),
#             )

#         except Exception as e:

#             print("========================================")
#             print("          EMAIL SEND ERROR")
#             print("========================================")
#             print("ERROR TYPE:", type(e).__name__)
#             print("ERROR:", repr(e))
#             print("ERROR STRING:", str(e))
#             print("========================================")

#             traceback.print_exc()

#             print("========================================")
#             print("Saving email as FAILED...")
#             print("========================================")

#             try:

#                 email.status = "failed"

#                 email.error_message = str(e)

#                 email.sent_at = None

#                 email.save(
#                     update_fields=[
#                         "status",
#                         "error_message",
#                         "sent_at"
#                     ]
#                 )

#                 print(
#                     "Email status saved as FAILED."
#                 )

#             except Exception as save_error:

#                 print(
#                     "ERROR SAVING FAILED EMAIL:",
#                     repr(save_error)
#                 )

#                 traceback.print_exc()

#             # -----------------------------------------
#             # Notification
#             # -----------------------------------------

#             try:

#                 Notification.objects.create(
#                     user=request.user,
#                     title="Email Failed",
#                     message=(
#                         f"Email '{email.subject}' "
#                         f"failed to send."
#                     ),
#                 )

#             except Exception as notification_error:

#                 print(
#                     "ERROR CREATING NOTIFICATION:",
#                     repr(notification_error)
#                 )

#                 traceback.print_exc()

#             return Response(
#                 {
#                     "error": "Failed to send email.",
#                     "details": str(e),
#                 },
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )

#         # ---------------------------------------------
#         # Response
#         # ---------------------------------------------

#         response_serializer = EmailSerializer(
#             email
#         )

#         return Response(
#             response_serializer.data,
#             status=status.HTTP_201_CREATED
#         )


# # =====================================================
# # EMAIL DETAIL
# # =====================================================

# class EmailDetailView(APIView):

#     permission_classes = [IsAuthenticated]

#     def get_object(self, pk):

#         try:

#             return Email.objects.select_related(
#                 "activity",
#                 "activity__created_by"
#             ).get(
#                 pk=pk
#             )

#         except Email.DoesNotExist:

#             return None

#     # =================================================
#     # GET
#     # =================================================

#     def get(self, request, pk):

#         email = self.get_object(pk)

#         if email is None:

#             return Response(
#                 {
#                     "detail": "Email not found."
#                 },
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         serializer = EmailSerializer(
#             email
#         )

#         return Response(
#             serializer.data,
#             status=status.HTTP_200_OK
#         )

#     # =================================================
#     # PUT
#     # =================================================

#     def put(self, request, pk):

#         email = self.get_object(pk)

#         if email is None:

#             return Response(
#                 {
#                     "detail": "Email not found."
#                 },
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         serializer = EmailSerializer(
#             email,
#             data=request.data,
#             partial=True
#         )

#         if serializer.is_valid():

#             serializer.save()

#             Notification.objects.create(
#                 user=request.user,
#                 title="Email Updated",
#                 message=(
#                     f"Email '{email.subject}' "
#                     f"has been updated."
#                 ),
#             )

#             return Response(
#                 EmailSerializer(email).data,
#                 status=status.HTTP_200_OK
#             )

#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )

#     # =================================================
#     # DELETE
#     # =================================================

#     def delete(self, request, pk):

#         email = self.get_object(pk)

#         if email is None:

#             return Response(
#                 {
#                     "detail": "Email not found."
#                 },
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         email_subject = email.subject

#         email.delete()

#         Notification.objects.create(
#             user=request.user,
#             title="Email Deleted",
#             message=(
#                 f"Email '{email_subject}' "
#                 f"has been deleted."
#             ),
#         )

#         return Response(
#             {
#                 "message": "Email deleted successfully."
#             },
#             status=status.HTTP_204_NO_CONTENT
#         )


# # =====================================================
# # EMAIL RECIPIENT
# # =====================================================

# class EmailRecipientView(APIView):

#     permission_classes = [IsAuthenticated]

#     def get(self, request, module, object_id):

#         module = module.lower().strip()

#         allowed_modules = [
#             "lead",
#             "deal",
#             "company",
#             "ticket",
#         ]

#         if module not in allowed_modules:

#             return Response(
#                 {
#                     "error": "Invalid module."
#                 },
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         try:

#             recipient = get_recipient_details(
#                 module,
#                 object_id
#             )

#             if not recipient.get("email"):

#                 return Response(
#                     {
#                         "error": (
#                             f"{module} with id "
#                             f"{object_id} does not have "
#                             f"a recipient email."
#                         )
#                     },
#                     status=status.HTTP_400_BAD_REQUEST
#                 )

#             return Response(
#                 recipient,
#                 status=status.HTTP_200_OK
#             )

#         except (
#             Lead.DoesNotExist,
#             Company.DoesNotExist,
#             Deal.DoesNotExist,
#             Ticket.DoesNotExist,
#         ):

#             return Response(
#                 {
#                     "error": (
#                         f"{module} with id "
#                         f"{object_id} not found."
#                     )
#                 },
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         except ValueError as error:

#             return Response(
#                 {
#                     "error": str(error)
#                 },
#                 status=status.HTTP_400_BAD_REQUEST
#             )



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.contrib.contenttypes.models import ContentType
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model

import traceback

from .models import Email
from .serializers import EmailSerializer

from apps.activities.activity.models import Activity
from apps.leads.models import Lead
from apps.deals.models import Deal
from apps.companies.models import Company
from apps.tickets.models import Ticket
from apps.notifications.models import Notification


User = get_user_model()


# ============================================================
# GET RECIPIENT DETAILS
# ============================================================

def get_recipient_details(module, object_id):
    """
    Get recipient name and email from Lead / Deal / Company / Ticket.
    """

    if module == "lead":
        obj = Lead.objects.get(id=object_id)

        name = f"{obj.first_name or ''} {obj.last_name or ''}".strip()

        return {
            "name": name,
            "email": obj.email,
            "object": obj,
        }

    elif module == "company":
        obj = Company.objects.get(id=object_id)

        return {
            "name": obj.company_name,
            "email": getattr(obj, "email", None),
            "object": obj,
        }

    elif module == "deal":
        obj = Deal.objects.select_related("associated_lead").get(
            id=object_id
        )

        lead = obj.associated_lead

        if not lead:
            return {
                "name": "",
                "email": None,
                "object": obj,
            }

        name = f"{lead.first_name or ''} {lead.last_name or ''}".strip()

        return {
            "name": name,
            "email": lead.email,
            "object": obj,
        }

    elif module == "ticket":
        obj = Ticket.objects.select_related(
            "associated_deal__associated_lead"
        ).get(id=object_id)

        deal = obj.associated_deal

        if not deal or not deal.associated_lead:
            return {
                "name": "",
                "email": None,
                "object": obj,
            }

        lead = deal.associated_lead

        name = f"{lead.first_name or ''} {lead.last_name or ''}".strip()

        return {
            "name": name,
            "email": lead.email,
            "object": obj,
        }

    raise ValueError(f"Invalid module: {module}")


# ============================================================
# EMAIL LIST + CREATE
# ============================================================

class EmailListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    # --------------------------------------------------------
    # GET EMAIL HISTORY
    # --------------------------------------------------------

    def get(self, request):

        emails = Email.objects.all().order_by(
            "-activity__created_at"
        )

        serializer = EmailSerializer(
            emails,
            many=True
        )

        return Response(serializer.data)

    # --------------------------------------------------------
    # SEND EMAIL
    # --------------------------------------------------------

    def post(self, request):

        data = request.data

        sender_id = data.get("sender_id")
        module = data.get("module")
        recipient_id = data.get("recipient_id")

        subject = data.get("subject")
        body = data.get("body")

        cc_emails = data.get("cc", [])
        bcc_emails = data.get("bcc", [])

        # ====================================================
        # BASIC VALIDATION
        # ====================================================

        if not sender_id:
            return Response(
                {
                    "error": "sender_id is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if not module:
            return Response(
                {
                    "error": "module is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if not recipient_id:
            return Response(
                {
                    "error": "recipient_id is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if not subject:
            return Response(
                {
                    "error": "Subject is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if not body:
            return Response(
                {
                    "error": "Email body is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # ====================================================
        # VALIDATE SENDER
        # ====================================================

        try:
            sender = User.objects.get(
                id=sender_id
            )

        except User.DoesNotExist:

            return Response(
                {
                    "error": "Sender not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # ====================================================
        # VALIDATE MODULE
        # ====================================================

        valid_modules = [
            "lead",
            "deal",
            "company",
            "ticket",
        ]

        if module not in valid_modules:

            return Response(
                {
                    "error": "Invalid module."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # ====================================================
        # GET RECIPIENT
        # ====================================================

        try:

            recipient_details = get_recipient_details(
                module,
                recipient_id
            )

            related_object = recipient_details["object"]
            recipient_email = recipient_details["email"]

        except Lead.DoesNotExist:

            return Response(
                {
                    "error": "Lead not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        except Deal.DoesNotExist:

            return Response(
                {
                    "error": "Deal not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        except Company.DoesNotExist:

            return Response(
                {
                    "error": "Company not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        except Ticket.DoesNotExist:

            return Response(
                {
                    "error": "Ticket not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        except ValueError as e:

            return Response(
                {
                    "error": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # ====================================================
        # VALIDATE RECIPIENT EMAIL
        # ====================================================

        if not recipient_email:

            return Response(
                {
                    "error": "Recipient email address is not available."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        recipient_email = str(
            recipient_email
        ).strip()

        if not recipient_email:

            return Response(
                {
                    "error": "Recipient email address is empty."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # ====================================================
        # VALIDATE CC / BCC
        # ====================================================

        if cc_emails is None:
            cc_emails = []

        if bcc_emails is None:
            bcc_emails = []

        if not isinstance(cc_emails, list):

            return Response(
                {
                    "error": "CC must be a list of email addresses."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if not isinstance(bcc_emails, list):

            return Response(
                {
                    "error": "BCC must be a list of email addresses."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Remove empty values
        cc_emails = [
            str(email).strip()
            for email in cc_emails
            if str(email).strip()
        ]

        bcc_emails = [
            str(email).strip()
            for email in bcc_emails
            if str(email).strip()
        ]

        # ====================================================
        # CONTENT TYPE
        # ====================================================

        content_type = ContentType.objects.get_for_model(
            related_object
        )

        # ====================================================
        # CREATE ACTIVITY
        # ====================================================

        activity = Activity.objects.create(
            activity_type="email",
            content_type=content_type,
            object_id=related_object.id,
            created_by=sender,
        )

        # ====================================================
        # CREATE EMAIL RECORD
        # ====================================================

        email_obj = Email.objects.create(
            activity=activity,
            sender=sender,
            recipient_email=recipient_email,
            subject=subject,
            body=body,
            cc=cc_emails,
            bcc=bcc_emails,
            status="draft",
        )

        # ====================================================
        # SMTP EMAIL
        # ====================================================

        try:

            print("")
            print("==========================================")
            print("          SMTP EMAIL DEBUG")
            print("==========================================")

            print(
                "EMAIL_BACKEND:",
                getattr(
                    settings,
                    "EMAIL_BACKEND",
                    None
                )
            )

            print(
                "EMAIL_HOST:",
                getattr(
                    settings,
                    "EMAIL_HOST",
                    None
                )
            )

            print(
                "EMAIL_PORT:",
                getattr(
                    settings,
                    "EMAIL_PORT",
                    None
                )
            )

            print(
                "EMAIL_USE_TLS:",
                getattr(
                    settings,
                    "EMAIL_USE_TLS",
                    None
                )
            )

            print(
                "EMAIL_USE_SSL:",
                getattr(
                    settings,
                    "EMAIL_USE_SSL",
                    None
                )
            )

            print(
                "EMAIL_HOST_USER:",
                getattr(
                    settings,
                    "EMAIL_HOST_USER",
                    None
                )
            )

            print(
                "EMAIL_PASSWORD_CONFIGURED:",
                bool(
                    getattr(
                        settings,
                        "EMAIL_HOST_PASSWORD",
                        None
                    )
                )
            )

            print(
                "DEFAULT_FROM_EMAIL:",
                getattr(
                    settings,
                    "DEFAULT_FROM_EMAIL",
                    None
                )
            )

            print(
                "RECIPIENT:",
                recipient_email
            )

            print(
                "CC:",
                cc_emails
            )

            print(
                "BCC:",
                bcc_emails
            )

            print("==========================================")

            # ------------------------------------------------
            # CREATE DJANGO EMAIL
            # ------------------------------------------------

            email_message = EmailMessage(
                subject=subject,
                body=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[recipient_email],
                cc=cc_emails,
                bcc=bcc_emails,
            )

            # ------------------------------------------------
            # SEND EMAIL
            # ------------------------------------------------

            result = email_message.send(
                fail_silently=False
            )

            print(
                "SMTP SEND RESULT:",
                result
            )

            print(
                "========== EMAIL SENT SUCCESSFULLY =========="
            )

            # ------------------------------------------------
            # UPDATE EMAIL STATUS
            # ------------------------------------------------

            email_obj.status = "sent"
            email_obj.sent_at = timezone.now()
            email_obj.error_message = None

            email_obj.save(
                update_fields=[
                    "status",
                    "sent_at",
                    "error_message",
                ]
            )

            # ------------------------------------------------
            # SUCCESS RESPONSE
            # ------------------------------------------------

            serializer = EmailSerializer(
                email_obj
            )

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        # ====================================================
        # SMTP ERROR
        # ====================================================

        except Exception as e:

            print("")
            print("==========================================")
            print("          SMTP EMAIL ERROR")
            print("==========================================")

            print(
                "ERROR TYPE:",
                type(e).__name__
            )

            print(
                "ERROR:",
                str(e)
            )

            print("TRACEBACK:")

            traceback.print_exc()

            print("==========================================")
            print("")

            # ------------------------------------------------
            # SAVE FAILED STATUS
            # ------------------------------------------------

            email_obj.status = "failed"
            email_obj.error_message = str(e)

            email_obj.save(
                update_fields=[
                    "status",
                    "error_message",
                ]
            )

            # ------------------------------------------------
            # CREATE NOTIFICATION
            # ------------------------------------------------

            try:

                Notification.objects.create(
                    user=sender,
                    title="Email Failed",
                    message=(
                        f"Failed to send email to "
                        f"{recipient_email}: "
                        f"{str(e)}"
                    ),
                    notification_type="email",
                )

            except Exception as notification_error:

                print(
                    "Notification creation failed:",
                    str(notification_error)
                )

            # ------------------------------------------------
            # ERROR RESPONSE
            # ------------------------------------------------

            return Response(
                {
                    "error": "Failed to send email.",
                    "details": str(e),
                    "error_type": type(e).__name__,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# ============================================================
# EMAIL DETAIL
# ============================================================

class EmailDetailView(APIView):

    permission_classes = [IsAuthenticated]

    # --------------------------------------------------------
    # GET
    # --------------------------------------------------------

    def get(self, request, pk):

        try:

            email_obj = Email.objects.get(
                pk=pk
            )

        except Email.DoesNotExist:

            return Response(
                {
                    "error": "Email not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = EmailSerializer(
            email_obj
        )

        return Response(
            serializer.data
        )

    # --------------------------------------------------------
    # PUT
    # --------------------------------------------------------

    def put(self, request, pk):

        try:

            email_obj = Email.objects.get(
                pk=pk
            )

        except Email.DoesNotExist:

            return Response(
                {
                    "error": "Email not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = EmailSerializer(
            email_obj,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # --------------------------------------------------------
    # DELETE
    # --------------------------------------------------------

    def delete(self, request, pk):

        try:

            email_obj = Email.objects.get(
                pk=pk
            )

        except Email.DoesNotExist:

            return Response(
                {
                    "error": "Email not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        email_obj.delete()

        return Response(
            {
                "message": "Email deleted successfully."
            },
            status=status.HTTP_204_NO_CONTENT
        )


# ============================================================
# EMAIL RECIPIENT
# ============================================================

class EmailRecipientView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        module = request.query_params.get(
            "module"
        )

        object_id = request.query_params.get(
            "objectId"
        )

        # ----------------------------------------------------
        # VALIDATE PARAMETERS
        # ----------------------------------------------------

        if not module:

            return Response(
                {
                    "error": "module is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if not object_id:

            return Response(
                {
                    "error": "objectId is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        valid_modules = [
            "lead",
            "deal",
            "company",
            "ticket",
        ]

        if module not in valid_modules:

            return Response(
                {
                    "error": "Invalid module."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # ----------------------------------------------------
        # GET RECIPIENT
        # ----------------------------------------------------

        try:

            recipient_details = get_recipient_details(
                module,
                object_id
            )

        except Lead.DoesNotExist:

            return Response(
                {
                    "error": "Lead not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        except Deal.DoesNotExist:

            return Response(
                {
                    "error": "Deal not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        except Company.DoesNotExist:

            return Response(
                {
                    "error": "Company not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        except Ticket.DoesNotExist:

            return Response(
                {
                    "error": "Ticket not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        except ValueError as e:

            return Response(
                {
                    "error": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # ----------------------------------------------------
        # CHECK EMAIL
        # ----------------------------------------------------

        recipient_email = recipient_details.get(
            "email"
        )

        if not recipient_email:

            return Response(
                {
                    "error": "Recipient email address is not available."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # ----------------------------------------------------
        # RESPONSE
        # ----------------------------------------------------

        return Response(
            {
                "name": recipient_details.get(
                    "name",
                    ""
                ),
                "email": recipient_email,
            },
            status=status.HTTP_200_OK
        )