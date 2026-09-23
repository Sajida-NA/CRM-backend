

# import json

# from django.conf import settings
# from django.contrib.contenttypes.models import ContentType

# from openai import OpenAI

# from apps.leads.models import Lead
# from apps.deals.models import Deal
# from apps.companies.models import Company
# from apps.tickets.models import Ticket

# from apps.activities.activity.models import Activity


# # =========================================================
# # USER HELPERS
# # =========================================================

# def get_user_name(user):
#     if not user:
#         return None

#     name = (
#         f"{getattr(user, 'first_name', '')} "
#         f"{getattr(user, 'last_name', '')}"
#     ).strip()

#     if name:
#         return name

#     return getattr(user, "email", None)


# def get_owner_names(users):
#     names = []

#     for user in users:
#         name = get_user_name(user)

#         if name:
#             names.append(name)

#     return names


# # =========================================================
# # ACTIVITY CONTEXT
# # =========================================================

# def get_activity_context(instance):
#     """
#     Get all activities connected to:
#     Lead / Deal / Company / Ticket
#     """

#     content_type = ContentType.objects.get_for_model(
#         instance.__class__
#     )

#     activities = (
#         Activity.objects
#         .filter(
#             content_type=content_type,
#             object_id=instance.id,
#         )
#         .select_related("created_by")
#         .prefetch_related(
#             "note",
#             "email",
#             "call",
#             "meeting",
#             "task",
#         )
#         .order_by("-created_at")
#     )

#     context = {
#         "notes": [],
#         "emails": [],
#         "calls": [],
#         "meetings": [],
#         "tasks": [],
#     }

#     for activity in activities:

#         # -------------------------------------------------
#         # NOTE
#         # -------------------------------------------------

#         if activity.activity_type == "note":
#             try:
#                 note = activity.note

#                 context["notes"].append({
#                     "created_at": (
#                         note.created_at.isoformat()
#                         if note.created_at
#                         else None
#                     ),
#                     "note": note.note,
#                 })

#             except Exception:
#                 pass

#         # -------------------------------------------------
#         # EMAIL
#         # -------------------------------------------------

#         elif activity.activity_type == "email":
#             try:
#                 email = activity.email

#                 context["emails"].append({
#                     "subject": email.subject,
#                     "body": email.body,
#                     "status": email.status,
#                     "sent_at": (
#                         email.sent_at.isoformat()
#                         if email.sent_at
#                         else None
#                     ),
#                     "to_recipients": email.to_recipients,
#                     "cc": email.cc,
#                     "bcc": email.bcc,
#                 })

#             except Exception:
#                 pass

#         # -------------------------------------------------
#         # CALL
#         # -------------------------------------------------

#         elif activity.activity_type == "call":
#             try:
#                 call = activity.call

#                 context["calls"].append({
#                     "date": str(call.date),
#                     "time": str(call.time),
#                     "call_mode": call.call_mode,
#                     "call_outcome": call.call_outcome,
#                     "twilio_status": call.twilio_status,
#                     "duration_seconds": call.duration,
#                     "note": call.note,
#                 })

#             except Exception:
#                 pass

#         # -------------------------------------------------
#         # MEETING
#         # -------------------------------------------------

#         elif activity.activity_type == "meeting":
#             try:
#                 meeting = activity.meeting

#                 context["meetings"].append({
#                     "title": meeting.title,

#                     "start_date": (
#                         str(meeting.start_date)
#                         if meeting.start_date
#                         else None
#                     ),

#                     "start_time": (
#                         str(meeting.start_time)
#                         if meeting.start_time
#                         else None
#                     ),

#                     "end_time": (
#                         str(meeting.end_time)
#                         if meeting.end_time
#                         else None
#                     ),

#                     "location": meeting.location,
#                     "reminder": meeting.reminder,
#                     "note": meeting.note,

#                     "owner": get_user_name(
#                         meeting.owner
#                     ),

#                     "attendees": get_owner_names(
#                         meeting.attendees.all()
#                     ),
#                 })

#             except Exception:
#                 pass

#         # -------------------------------------------------
#         # TASK
#         # -------------------------------------------------

#         elif activity.activity_type == "task":
#             try:
#                 task = activity.task

#                 context["tasks"].append({
#                     "task_name": task.task_name,

#                     "due_date": (
#                         str(task.due_date)
#                         if task.due_date
#                         else None
#                     ),

#                     "time": (
#                         str(task.time)
#                         if task.time
#                         else None
#                     ),

#                     "task_type": task.task_type,
#                     "priority": task.priority,

#                     "assigned_to": get_owner_names(
#                         task.assigned_to.all()
#                     ),

#                     "note": task.note,
#                 })

#             except Exception:
#                 pass

#     return context


# # =========================================================
# # LEAD CONTEXT
# # =========================================================

# def build_lead_context(lead_id):

#     lead = (
#         Lead.objects
#         .select_related("company")
#         .prefetch_related("contact_owners")
#         .filter(pk=lead_id)
#         .first()
#     )

#     if not lead:
#         raise ValueError("Lead not found.")

#     lead_name = (
#         f"{getattr(lead, 'first_name', '')} "
#         f"{getattr(lead, 'last_name', '')}"
#     ).strip()

#     context = {
#         "lead": {
#             "id": lead.id,
#             "name": lead_name,
#             "email": getattr(lead, "email", None),
#             "phone_number": getattr(
#                 lead,
#                 "phone_number",
#                 None,
#             ),
#             "job_title": getattr(
#                 lead,
#                 "job_title",
#                 None,
#             ),
#             "status": getattr(
#                 lead,
#                 "lead_status",
#                 None,
#             ),
#             "city": getattr(
#                 lead,
#                 "city",
#                 None,
#             ),
#             "company": (
#                 lead.company.company_name
#                 if getattr(lead, "company", None)
#                 else None
#             ),
#             "contact_owners": get_owner_names(
#                 lead.contact_owners.all()
#             ),
#         },

#         "activities": get_activity_context(lead),
#     }

#     return context


# # =========================================================
# # DEAL CONTEXT
# # =========================================================

# def build_deal_context(deal_id):

#     deal = (
#         Deal.objects
#         .select_related(
#             "associated_lead",
#             "associated_lead__company",
#         )
#         .prefetch_related("deal_owners")
#         .filter(pk=deal_id)
#         .first()
#     )

#     if not deal:
#         raise ValueError("Deal not found.")

#     lead = deal.associated_lead

#     lead_name = None

#     if lead:
#         lead_name = (
#             f"{getattr(lead, 'first_name', '')} "
#             f"{getattr(lead, 'last_name', '')}"
#         ).strip()

#     context = {
#         "deal": {
#             "id": deal.id,
#             "name": deal.deal_name,
#             "stage": deal.deal_stage,
#             "amount": str(deal.amount),
#             "priority": deal.priority,
#             "close_date": str(deal.close_date),

#             "created_date": (
#                 deal.created_date.isoformat()
#                 if deal.created_date
#                 else None
#             ),

#             "updated_at": (
#                 deal.updated_at.isoformat()
#                 if deal.updated_at
#                 else None
#             ),

#             "deal_owners": get_owner_names(
#                 deal.deal_owners.all()
#             ),
#         },

#         "associated_lead": {
#             "id": lead.id if lead else None,
#             "name": lead_name,

#             "email": (
#                 getattr(lead, "email", None)
#                 if lead
#                 else None
#             ),

#             "company": (
#                 lead.company.company_name
#                 if lead
#                 and getattr(lead, "company", None)
#                 else None
#             ),
#         },

#         "activities": get_activity_context(deal),
#     }

#     return context


# # =========================================================
# # COMPANY CONTEXT
# # =========================================================

# def build_company_context(company_id):

#     company = (
#         Company.objects
#         .select_related("company_owner")
#         .filter(pk=company_id)
#         .first()
#     )

#     if not company:
#         raise ValueError("Company not found.")

#     context = {
#         "company": {
#             "id": company.id,
#             "name": company.company_name,
#             "domain_name": company.domain_name,
#             "industry": company.industry,
#             "type": company.type,
#             "city": company.city,
#             "country_region": company.country_region,
#             "no_of_employees": company.no_of_employees,

#             "annual_revenue": (
#                 str(company.annual_revenue)
#                 if company.annual_revenue is not None
#                 else None
#             ),

#             "phone_number": company.phone_number,
#             "email": company.email,

#             "company_owner": get_user_name(
#                 company.company_owner
#             ),

#             "created_date": (
#                 company.created_date.isoformat()
#                 if company.created_date
#                 else None
#             ),

#             "updated_at": (
#                 company.updated_at.isoformat()
#                 if company.updated_at
#                 else None
#             ),
#         },

#         "activities": get_activity_context(company),
#     }

#     return context


# # =========================================================
# # TICKET CONTEXT
# # =========================================================

# def build_ticket_context(ticket_id):

#     ticket = (
#         Ticket.objects
#         .select_related(
#             "associated_deal",
#             "associated_deal__associated_lead",
#             "associated_deal__associated_lead__company",
#         )
#         .prefetch_related("ticket_owners")
#         .filter(pk=ticket_id)
#         .first()
#     )

#     if not ticket:
#         raise ValueError("Ticket not found.")

#     deal = ticket.associated_deal

#     lead = (
#         deal.associated_lead
#         if deal
#         else None
#     )

#     lead_name = None

#     if lead:
#         lead_name = (
#             f"{getattr(lead, 'first_name', '')} "
#             f"{getattr(lead, 'last_name', '')}"
#         ).strip()

#     context = {
#         "ticket": {
#             "id": ticket.id,
#             "name": ticket.ticket_name,
#             "description": ticket.description,
#             "status": ticket.ticket_status,
#             "source": ticket.source,
#             "priority": ticket.priority,

#             "ticket_owners": get_owner_names(
#                 ticket.ticket_owners.all()
#             ),

#             "created_date": (
#                 ticket.created_date.isoformat()
#                 if ticket.created_date
#                 else None
#             ),

#             "updated_at": (
#                 ticket.updated_at.isoformat()
#                 if ticket.updated_at
#                 else None
#             ),
#         },

#         "associated_deal": {
#             "id": deal.id if deal else None,

#             "name": (
#                 deal.deal_name
#                 if deal
#                 else None
#             ),

#             "stage": (
#                 deal.deal_stage
#                 if deal
#                 else None
#             ),

#             "amount": (
#                 str(deal.amount)
#                 if deal
#                 else None
#             ),
#         },

#         "associated_lead": {
#             "id": lead.id if lead else None,
#             "name": lead_name,

#             "email": (
#                 getattr(lead, "email", None)
#                 if lead
#                 else None
#             ),

#             "company": (
#                 lead.company.company_name
#                 if lead
#                 and getattr(lead, "company", None)
#                 else None
#             ),
#         },

#         "activities": get_activity_context(ticket),
#     }

#     return context


# # =========================================================
# # AI SUMMARY GENERATOR
# # =========================================================

# def generate_ai_summary(context, module):

#     api_key = getattr(
#         settings,
#         "OPENAI_API_KEY",
#         "",
#     )

#     if not api_key:
#         raise ValueError(
#             "OPENAI_API_KEY is not configured."
#         )

#     client = OpenAI(
#         api_key=api_key
#     )

#     crm_data = json.dumps(
#         context,
#         indent=2,
#         default=str,
#         ensure_ascii=False,
#     )

#     module_names = {
#         "lead": "lead",
#         "deal": "deal",
#         "company": "company",
#         "ticket": "ticket",
#     }

#     entity_name = module_names.get(
#         module,
#         "CRM record",
#     )

#     prompt = f"""
# You are an AI assistant inside a CRM system.

# Create a concise, professional and factual summary
# for this {entity_name}.

# IMPORTANT RULES:

# 1. Use ONLY the CRM data provided below.

# 2. NEVER invent information.

# 3. NEVER assume that a customer said, requested,
# wanted, agreed to, rejected, or showed interest
# in something unless that information is explicitly
# present in the CRM data.

# 4. NEVER create activities that are not present.

# 5. If there are no activities, clearly say that there
# are no activities recorded for this record.

# 6. Use the entity's actual name when available.

# 7. Mention the current status or stage when available.

# 8. Mention important recent notes, emails, calls,
# meetings and tasks when they exist.

# 9. Mention pending or upcoming tasks only when they
# are explicitly present.

# 10. Mention customer requirements, concerns,
# interest, objections or follow-up needs only when
# explicitly supported by the CRM data.

# 11. Do not confuse associated Lead, Deal, Company
# or Ticket information with an activity.

# 12. Do not make unsupported recommendations.

# 13. Keep the summary concise and useful for a CRM user.

# 14. Return ONLY the summary paragraph.

# 15. Do not use markdown headings.

# CRM DATA:

# {crm_data}
# """

#     try:
#         response = client.responses.create(
#             model="gpt-5.6-luna",
#             input=prompt,
#         )

#     except Exception as exc:
#         raise RuntimeError(
#             f"OpenAI API error: {type(exc).__name__}: {str(exc)}"
#         ) from exc

#     summary = (
#         response.output_text
#         if hasattr(response, "output_text")
#         else ""
#     )

#     summary = summary.strip()

#     if not summary:
#         return (
#             "There is not enough information available "
#             "to generate a comprehensive summary."
#         )

#     return summary



import time

from google import genai
from decouple import config


# =========================================================
# GEMINI CONFIGURATION
# =========================================================

GEMINI_API_KEY = config(
    "GEMINI_API_KEY",
    default=""
)

PRIMARY_MODEL = "gemini-3.5-flash-lite"
FALLBACK_MODEL = "gemini-3.5-flash"

client = None

if GEMINI_API_KEY:
    client = genai.Client(
        api_key=GEMINI_API_KEY
    )


# =========================================================
# GENERATE AI SUMMARY
# =========================================================

def generate_ai_summary(data):

    if not GEMINI_API_KEY:
        raise Exception(
            "GEMINI_API_KEY is not configured."
        )

    if client is None:
        raise Exception(
            "Gemini client is not initialized."
        )

    if not data:
        raise Exception(
            "CRM data is empty."
        )

    module = data.get(
        "module",
        "CRM"
    )

    object_id = data.get(
        "object_id"
    )

    crm_data = data.get(
        "crm_data"
    )

    if not crm_data:
        raise Exception(
            "CRM record data is empty."
        )

    # =====================================================
    # MODULE NAME
    # =====================================================

    module_names = {
        "lead": "Lead",
        "company": "Company",
        "deal": "Deal",
        "ticket": "Ticket",
    }

    module_name = module_names.get(
        module,
        str(module).title()
    )

    # =====================================================
    # PROMPT
    # =====================================================

    prompt = f"""
You are an AI assistant inside a CRM system.

Create a concise and professional summary of this CRM record.

CRM MODULE:
{module_name}

CRM RECORD ID:
{object_id}

CRM RECORD DATA:
{crm_data}

RULES:

1. Use ONLY the information provided.
2. Never invent information.
3. Do not create fake activities.
4. Do not assume missing information.
5. Keep the summary concise.
6. Adapt the summary to the CRM module.
7. Focus on information useful to a CRM user.

Return:

Summary:
A brief overview of the record.

Key Information:
- Important information
- Important business/customer details
- Current status/stage if available

Current Status:
The current status based only on the provided data.

Next Actions:
- Practical next actions based only on the available information.

If information is unavailable, omit it.
"""

    # =====================================================
    # MODELS
    # =====================================================

    models = [
        PRIMARY_MODEL,
        FALLBACK_MODEL,
    ]

    last_error = None

    # =====================================================
    # TRY MODELS
    # =====================================================

    for model in models:

        for attempt in range(3):

            try:

                print(
                    f"Trying Gemini model: {model} "
                    f"(attempt {attempt + 1}/3)"
                )

                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                )

                summary = response.text

                if not summary:
                    raise Exception(
                        "Gemini returned an empty response."
                    )

                print(
                    f"Gemini success using model: {model}"
                )

                return summary.strip()

            except Exception as e:

                last_error = e

                error_text = str(e)

                print(
                    f"Gemini error using {model}: "
                    f"{error_text}"
                )

                # =================================================
                # RETRY TEMPORARY ERRORS
                # =================================================

                temporary_error = (
                    "503" in error_text
                    or "UNAVAILABLE" in error_text
                    or "high demand" in error_text.lower()
                    or "temporarily" in error_text.lower()
                )

                if temporary_error:

                    if attempt < 2:

                        wait_time = 2 ** attempt

                        print(
                            f"Gemini temporarily unavailable. "
                            f"Retrying in {wait_time} seconds..."
                        )

                        time.sleep(
                            wait_time
                        )

                        continue

                # =================================================
                # MOVE TO FALLBACK MODEL
                # =================================================

                break

    # =========================================================
    # ALL MODELS FAILED
    # =========================================================

    raise Exception(
        f"Gemini AI error: {str(last_error)}"
    )