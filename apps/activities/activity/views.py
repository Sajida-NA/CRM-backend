# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated

# from django.contrib.contenttypes.models import ContentType

# from .models import Activity


# # =====================================================
# # GET ALL ACTIVITIES FOR A MODULE RECORD
# # Example:
# # GET /api/activities/timeline/lead/4/
# # =====================================================

# class ActivityTimelineView(APIView):

#     permission_classes = [IsAuthenticated]

#     def get(self, request, module, module_id):

#         # =====================================================
#         # FIND CONTENT TYPE
#         # =====================================================

#         if module == "lead":

#             content_type = ContentType.objects.get(
#                 app_label="leads",
#                 model="lead"
#             )

#         elif module == "deal":

#             content_type = ContentType.objects.get(
#                 app_label="deals",
#                 model="deal"
#             )

#         elif module == "company":

#             content_type = ContentType.objects.get(
#                 app_label="companies",
#                 model="company"
#             )

#         elif module == "ticket":

#             content_type = ContentType.objects.get(
#                 app_label="tickets",
#                 model="ticket"
#             )

#         else:

#             return Response(
#                 {
#                     "error": "Invalid module."
#                 },
#                 status=400
#             )

#         # =====================================================
#         # GET ALL ACTIVITIES
#         # =====================================================

#         activities = (
#             Activity.objects.filter(
#                 content_type=content_type,
#                 object_id=module_id
#             )
#             .select_related("created_by")
#             .order_by("-created_at")
#         )

#         response = []

#         # =====================================================
#         # LOOP THROUGH ACTIVITIES
#         # =====================================================

#         for activity in activities:

#             data = {
#                 "activity_type": activity.activity_type,

#                 "created_at": activity.created_at,

#                 "created_by": (
#                     activity.created_by.get_full_name()
#                     or activity.created_by.email
#                     if activity.created_by
#                     else None
#                 ),
#             }

#             # =================================================
#             # NOTE
#             # =================================================

#             if activity.activity_type == "note":

#                 if hasattr(activity, "note"):

#                     note = activity.note

#                     data["note"] = {
#                         "id": note.id,
#                         "title": "Note",
#                         "note": note.note,
#                     }

#             # =================================================
#             # CALL
#             # =================================================

#             elif activity.activity_type == "call":

#                 if hasattr(activity, "call"):

#                     call = activity.call

#                     data["call"] = {
#                         "id": call.id,
#                         "call_outcome": call.call_outcome,
#                     }

#             # =================================================
#             # TASK
#             # =================================================

#             elif activity.activity_type == "task":

#                 if hasattr(activity, "task"):

#                     task = activity.task

#                     data["task"] = {
#                         "id": task.id,
#                         "task_name": task.task_name,
#                         "due_date": task.due_date,
#                         "time": task.time,
#                         "task_type": task.task_type,
#                         "priority": task.priority,

#                         "assigned_to": (
#                             task.assigned_to.get_full_name()
#                             or task.assigned_to.email
#                             if task.assigned_to
#                             else None
#                         ),
#                     }

#             # =================================================
#             # MEETING
#             # =================================================

#             elif activity.activity_type == "meeting":

#                 if hasattr(activity, "meeting"):

#                     meeting = activity.meeting

#                     data["meeting"] = {
#                         "id": meeting.id,

#                         "title": meeting.title,

#                         "owner": (
#                             meeting.owner.get_full_name()
#                             or meeting.owner.email
#                             if meeting.owner
#                             else None
#                         ),

#                         "start_date": meeting.start_date,

#                         "start_time": meeting.start_time,

#                         "end_time": meeting.end_time,

#                         "location": meeting.location,

#                         "reminder": meeting.reminder,

#                         "note": meeting.note,

#                         "attendees": [
#                             {
#                                 "id": user.id,

#                                 "name": (
#                                     user.get_full_name()
#                                     or user.email
#                                 )
#                             }
#                             for user in meeting.attendees.all()
#                         ],
#                     }

#             # =================================================
#             # EMAIL
#             # =================================================

#             elif activity.activity_type == "email":

#                 if hasattr(activity, "email"):

#                     email = activity.email

#                     data["email"] = {
#                         "id": email.id,

#                         "subject": email.subject,

#                         "body": email.body,

#                         "status": email.status,

#                         "to_recipients": email.to_recipients,

#                         "cc": email.cc,

#                         "bcc": email.bcc,

#                         "sent_at": email.sent_at,

#                         "error_message": email.error_message,
#                     }

#             # =================================================
#             # ADD ACTIVITY TO RESPONSE
#             # =====================================================

#             response.append(data)

#         # =====================================================
#         # FINAL RESPONSE
#         # =====================================================

#         return Response(response)


# # =====================================================
# # GET ACTIVITIES OF ONE SPECIFIC TYPE WITH FULL DETAILS
# #
# # Example:
# # GET /api/activities/lead/4/note/
# # GET /api/activities/deal/4/call/
# # GET /api/activities/lead/4/task/
# # =====================================================

# class ActivityTypeDetailView(APIView):

#     permission_classes = [IsAuthenticated]

#     def get(self, request, module, module_id, activity_type):

#         # =====================================================
#         # VALID ACTIVITY TYPES
#         # =====================================================

#         valid_activity_types = [
#             "note",
#             "call",
#             "task",
#             "meeting",
#             "email",
#         ]

#         if activity_type not in valid_activity_types:

#             return Response(
#                 {
#                     "error": "Invalid activity type."
#                 },
#                 status=400
#             )

#         # =====================================================
#         # FIND CONTENT TYPE
#         # =====================================================

#         if module == "lead":

#             content_type = ContentType.objects.get(
#                 app_label="leads",
#                 model="lead"
#             )

#         elif module == "deal":

#             content_type = ContentType.objects.get(
#                 app_label="deals",
#                 model="deal"
#             )

#         elif module == "company":

#             content_type = ContentType.objects.get(
#                 app_label="companies",
#                 model="company"
#             )

#         elif module == "ticket":

#             content_type = ContentType.objects.get(
#                 app_label="tickets",
#                 model="ticket"
#             )

#         else:

#             return Response(
#                 {
#                     "error": "Invalid module."
#                 },
#                 status=400
#             )

#         # =====================================================
#         # GET ACTIVITIES OF THE REQUESTED TYPE
#         # =====================================================

#         activities = (
#             Activity.objects.filter(
#                 content_type=content_type,
#                 object_id=module_id,
#                 activity_type=activity_type
#             )
#             .select_related("created_by")
#             .order_by("-created_at")
#         )

#         response = []

#         # =====================================================
#         # LOOP THROUGH ACTIVITIES
#         # =====================================================

#         for activity in activities:

#             data = {
#                 "activity_type": activity.activity_type,

#                 "created_at": activity.created_at,

#                 "created_by": (
#                     activity.created_by.get_full_name()
#                     or activity.created_by.email
#                     if activity.created_by
#                     else None
#                 ),
#             }

#             # =================================================
#             # NOTE
#             # =================================================

#             if activity.activity_type == "note":

#                 if hasattr(activity, "note"):

#                     note = activity.note

#                     data["note"] = {
#                         "id": note.id,
#                         "title": "Note",
#                         "note": note.note,
#                     }

#             # =================================================
#             # CALL
#             # =================================================

#             elif activity.activity_type == "call":

#                 if hasattr(activity, "call"):

#                     call = activity.call

#                     data["call"] = {
#                         "id": call.id,
#                         "call_outcome": call.call_outcome,
#                     }

#             # =================================================
#             # TASK
#             # =================================================

#             elif activity.activity_type == "task":

#                 if hasattr(activity, "task"):

#                     task = activity.task

#                     data["task"] = {
#                         "id": task.id,
#                         "task_name": task.task_name,
#                         "due_date": task.due_date,
#                         "time": task.time,
#                         "task_type": task.task_type,
#                         "priority": task.priority,

#                         "assigned_to": (
#                             task.assigned_to.get_full_name()
#                             or task.assigned_to.email
#                             if task.assigned_to
#                             else None
#                         ),
#                     }

#             # =================================================
#             # MEETING
#             # =================================================

#             elif activity.activity_type == "meeting":

#                 if hasattr(activity, "meeting"):

#                     meeting = activity.meeting

#                     data["meeting"] = {
#                         "id": meeting.id,

#                         "title": meeting.title,

#                         "owner": (
#                             meeting.owner.get_full_name()
#                             or meeting.owner.email
#                             if meeting.owner
#                             else None
#                         ),

#                         "start_date": meeting.start_date,

#                         "start_time": meeting.start_time,

#                         "end_time": meeting.end_time,

#                         "location": meeting.location,

#                         "reminder": meeting.reminder,

#                         "note": meeting.note,

#                         "attendees": [
#                             {
#                                 "id": user.id,

#                                 "name": (
#                                     user.get_full_name()
#                                     or user.email
#                                 )
#                             }
#                             for user in meeting.attendees.all()
#                         ],
#                     }

#             # =================================================
#             # EMAIL
#             # =================================================

#             elif activity.activity_type == "email":

#                 if hasattr(activity, "email"):

#                     email = activity.email

#                     data["email"] = {
#                         "id": email.id,

#                         "subject": email.subject,

#                         "body": email.body,

#                         "status": email.status,

#                         "to_recipients": email.to_recipients,

#                         "cc": email.cc,

#                         "bcc": email.bcc,

#                         "sent_at": email.sent_at,

#                         "error_message": email.error_message,
#                     }

#             # =================================================
#             # ADD ACTIVITY TO RESPONSE
#             # =====================================================

#             response.append(data)

#         # =====================================================
#         # FINAL RESPONSE
#         # =====================================================

#         return Response({
#             "module": module,
#             "module_id": module_id,
#             "activity_type": activity_type,
#             "activities": response
#         })



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.contrib.contenttypes.models import ContentType

from .models import Activity
from .serializers import ActivitySerializer


class ActivityTimelineView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, module, module_id):

        module_map = {
            "lead": ("leads", "lead"),
            "deal": ("deals", "deal"),
            "company": ("companies", "company"),
            "ticket": ("tickets", "ticket"),
        }

        if module not in module_map:
            return Response(
                {
                    "error": "Invalid module."
                },
                status=400
            )

        app_label, model = module_map[module]

        content_type = ContentType.objects.get(
            app_label=app_label,
            model=model
        )

        activities = (
            Activity.objects
            .filter(
                content_type=content_type,
                object_id=module_id
            )
            .select_related("created_by")
            .order_by("-created_at")
        )

        serializer = ActivitySerializer(
            activities,
            many=True
        )

        return Response(serializer.data)