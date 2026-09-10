

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.contrib.contenttypes.models import ContentType
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model

from .models import Email
from .serializers import EmailSerializer

from apps.activities.activity.models import Activity
from apps.leads.models import Lead
from apps.deals.models import Deal
from apps.companies.models import Company
from apps.tickets.models import Ticket

from apps.notifications.models import Notification

# If these models exist in your project,
# import them here.
# from apps.companies.models import Company
# from apps.tickets.models import Ticket


User = get_user_model()

# =====================================================
# GET RECIPIENT DETAILS
# =====================================================

def get_recipient_details(module, object_id):

    module = module.lower().strip()

    # =================================================
    # LEAD
    # =================================================

    if module == "lead":

        lead = Lead.objects.get(pk=object_id)

        return {
            "id": lead.id,
            "name": (
                f"{lead.first_name} {lead.last_name}"
            ).strip(),
            "email": lead.email,
        }

    # =================================================
    # COMPANY
    # =================================================

    elif module == "company":

        company = Company.objects.get(pk=object_id)

        return {
            "id": company.id,
            "name": company.company_name,
            "email": company.email,
        }

    # =================================================
    # DEAL
    # =================================================

    elif module == "deal":

        deal = Deal.objects.select_related(
            "associated_lead"
        ).get(pk=object_id)

        lead = deal.associated_lead

        return {
            "id": deal.id,
            "name": (
                f"{lead.first_name} {lead.last_name}"
            ).strip(),
            "email": lead.email,
        }

    # =================================================
    # TICKET
    # =================================================

    elif module == "ticket":

        ticket = Ticket.objects.select_related(
            "associated_deal__associated_lead"
        ).get(pk=object_id)

        lead = (
            ticket.associated_deal.associated_lead
        )

        return {
            "id": ticket.id,
            "name": (
                f"{lead.first_name} {lead.last_name}"
            ).strip(),
            "email": lead.email,
        }

    raise ValueError("Invalid module")


class EmailListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    # ==========================================
    # GET
    # ==========================================

    def get(self, request):

        emails = Email.objects.select_related(
            "activity",
            "activity__created_by"
        ).order_by(
            "-activity__created_at"
        )

        serializer = EmailSerializer(
            emails,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    # ==========================================
    # POST
    # ==========================================

    def post(self, request):

        # --------------------------------------
        # Get request data
        # --------------------------------------

        sender_id = request.data.get("sender_id")
        module = request.data.get("module")
        recipient_id = request.data.get("recipient_id")

        # --------------------------------------
        # Validate sender_id
        # --------------------------------------

        if not sender_id:

            return Response(
                {
                    "error": "sender_id is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            sender = User.objects.get(
                pk=sender_id
            )

        except User.DoesNotExist:

            return Response(
                {
                    "error": f"User with id {sender_id} not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # --------------------------------------
        # Validate module
        # --------------------------------------

        if not module:

            return Response(
                {
                    "error": "module is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        module = module.lower().strip()

        allowed_modules = [
            "lead",
            "deal",
            "company",
            "ticket",
        ]

        if module not in allowed_modules:

            return Response(
                {
                    "error": (
                        "module must be 'lead', 'deal', "
                        "'company', or 'ticket'."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # --------------------------------------
        # Validate recipient_id
        # --------------------------------------

        if not recipient_id:

            return Response(
                {
                    "error": "recipient_id is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # --------------------------------------
        # Select CRM model
        # --------------------------------------

        if module == "lead":

            model = Lead

        elif module == "deal":

            model = Deal

        elif module == "company":

            from apps.companies.models import Company

            model = Company

        elif module == "ticket":

            from apps.tickets.models import Ticket

            model = Ticket

        # --------------------------------------
        # Get recipient CRM object
        # --------------------------------------

        try:

            related_object = model.objects.get(
                pk=recipient_id
            )

        except model.DoesNotExist:

            return Response(
                {
                    "error": (
                        f"{module} with id "
                        f"{recipient_id} not found."
                    )
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # --------------------------------------
        # Get recipient name and email
        # --------------------------------------

        recipient_name = None
        recipient_email = None

        # --------------------------------------
        # Lead
        # --------------------------------------

        if module == "lead":

            recipient_name = (
                f"{related_object.first_name} "
                f"{related_object.last_name}"
            ).strip()

            recipient_email = related_object.email

        # --------------------------------------
        # Deal
        # --------------------------------------

        elif module == "deal":

            lead = related_object.associated_lead

            if lead:

                recipient_name = (
                    f"{lead.first_name} "
                    f"{lead.last_name}"
                ).strip()

                recipient_email = lead.email

        # --------------------------------------
        # Company
        # --------------------------------------

        elif module == "company":

            recipient_name = getattr(
                related_object,
                "name",
                None
            )

            recipient_email = getattr(
                related_object,
                "email",
                None
            )

        # --------------------------------------
        # Ticket
        # --------------------------------------

        elif module == "ticket":

            ticket_owner = getattr(
                related_object,
                "ticket_owner",
                None
            )

            if ticket_owner:

                recipient_name = (
                    ticket_owner.get_full_name()
                    or ticket_owner.email
                )

                recipient_email = (
                    ticket_owner.email
                )

        # --------------------------------------
        # Make sure recipient has email
        # --------------------------------------

        if not recipient_email:

            return Response(
                {
                    "error": (
                        f"{module} with id "
                        f"{recipient_id} does not have "
                        f"a recipient email."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # --------------------------------------
        # Validate email fields
        # --------------------------------------

        subject = request.data.get(
            "subject",
            ""
        )

        body = request.data.get(
            "body",
            ""
        )

        cc = request.data.get(
            "cc",
            []
        )

        bcc = request.data.get(
            "bcc",
            []
        )

        if not isinstance(cc, list):

            return Response(
                {
                    "error": "cc must be a list."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if not isinstance(bcc, list):

            return Response(
                {
                    "error": "bcc must be a list."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # --------------------------------------
        # Create ContentType
        # --------------------------------------

        content_type = ContentType.objects.get_for_model(
            model
        )

        # --------------------------------------
        # Create Activity
        # --------------------------------------

        activity = Activity.objects.create(
            activity_type="email",
            created_by=sender,
            content_type=content_type,
            object_id=related_object.pk
        )

        # --------------------------------------
        # Create recipient data
        # --------------------------------------

        to_recipients = [
            {
                "id": related_object.pk,
                "name": recipient_name,
                "email": recipient_email,
            }
        ]

        # --------------------------------------
        # Convert CC emails
        # --------------------------------------

        cc_emails = []

        for recipient in cc:

            if isinstance(recipient, dict):

                email_address = recipient.get(
                    "email"
                )

                if email_address:
                    cc_emails.append(
                        email_address
                    )

            elif isinstance(recipient, str):

                cc_emails.append(recipient)

        # --------------------------------------
        # Convert BCC emails
        # --------------------------------------

        bcc_emails = []

        for recipient in bcc:

            if isinstance(recipient, dict):

                email_address = recipient.get(
                    "email"
                )

                if email_address:
                    bcc_emails.append(
                        email_address
                    )

            elif isinstance(recipient, str):

                bcc_emails.append(recipient)

        # --------------------------------------
        # Create Email object
        # --------------------------------------

        email = Email.objects.create(
            activity=activity,
            to_recipients=to_recipients,
            cc=cc,
            bcc=bcc,
            subject=subject,
            body=body,
            status="draft"
        )

        # --------------------------------------
        # Send email
        # --------------------------------------

        try:

            email_message = EmailMessage(
                subject=subject,
                body=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[recipient_email],
                cc=cc_emails,
                bcc=bcc_emails
            )

            email_message.send(
                fail_silently=False
            )

            # ----------------------------------
            # Success
            # ----------------------------------

            email.status = "sent"

            email.sent_at = timezone.now()

            email.error_message = None

            email.save(
                update_fields=[
                    "status",
                    "sent_at",
                    "error_message"
                ]
            )

            Notification.objects.create(
                user=request.user,
                title="Email Sent",
                message=f"Email '{email.subject}' has been sent successfully.",
            )

        except Exception as e:

            # ----------------------------------
            # Failed
            # ----------------------------------

            email.status = "failed"

            email.error_message = str(e)

            email.sent_at = None

            email.save(
                update_fields=[
                    "status",
                    "error_message",
                    "sent_at"
                ]
            )

            Notification.objects.create(
                user=request.user,
                title="Email Failed",
                message=f"Email '{email.subject}' failed to send.",
            )

        # --------------------------------------
        # Response
        # --------------------------------------

        response_serializer = EmailSerializer(
            email
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )


class EmailDetailView(APIView):

    permission_classes = [IsAuthenticated]

    # ==========================================
    # Get email
    # ==========================================

    def get_object(self, pk):

        try:

            return Email.objects.select_related(
                "activity",
                "activity__created_by"
            ).get(
                pk=pk
            )

        except Email.DoesNotExist:

            return None

    # ==========================================
    # GET
    # ==========================================

    def get(self, request, pk):

        email = self.get_object(pk)

        if email is None:

            return Response(
                {
                    "detail": "Email not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = EmailSerializer(
            email
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    # ==========================================
    # PUT
    # ==========================================

    def put(self, request, pk):

        email = self.get_object(pk)

        if email is None:

            return Response(
                {
                    "detail": "Email not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = EmailSerializer(
            email,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            Notification.objects.create(
               user=request.user,
               title="Email Updated",
               message=f"Email '{email.subject}' has been updated.",
            )

            return Response(
                EmailSerializer(email).data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # ==========================================
    # DELETE
    # ==========================================

    def delete(self, request, pk):

        email = self.get_object(pk)

        if email is None:

            return Response(
                {
                    "detail": "Email not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        email_subject = email.subject

        email.delete()

        Notification.objects.create(
           user=request.user,
           title="Email Deleted",
           message=f"Email '{email_subject}' has been deleted.",
        )

        return Response(
            {
                "message": "Email deleted successfully."
            },
            status=status.HTTP_204_NO_CONTENT
        )


class EmailRecipientView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, module, object_id):

        module = module.lower().strip()

        allowed_modules = [
            "lead",
            "deal",
            "company",
            "ticket",
        ]

        if module not in allowed_modules:

            return Response(
                {
                    "error": "Invalid module."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            recipient = get_recipient_details(
                module,
                object_id
            )

            return Response(
                recipient,
                status=status.HTTP_200_OK
            )

        except (
            Lead.DoesNotExist,
            Company.DoesNotExist,
            Deal.DoesNotExist,
            Ticket.DoesNotExist,
        ):

            return Response(
                {
                    "error": (
                        f"{module} with id "
                        f"{object_id} not found."
                    )
                },
                status=status.HTTP_404_NOT_FOUND
            )

        except ValueError as error:

            return Response(
                {
                    "error": str(error)
                },
                status=status.HTTP_400_BAD_REQUEST
            )