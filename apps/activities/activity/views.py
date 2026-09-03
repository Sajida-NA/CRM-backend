

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework import status

# from django.contrib.contenttypes.models import ContentType

# from .models import Activity
# from .serializers import ActivitySerializer


# # =====================================================
# # MODULE → CONTENT TYPE
# # =====================================================

# MODULE_CONTENT_TYPES = {
#     "lead": ("leads", "lead"),
#     "deal": ("deals", "deal"),
#     "company": ("companies", "company"),
#     "ticket": ("tickets", "ticket"),
# }


# # =====================================================
# # GET CONTENT TYPE
# # =====================================================

# def get_content_type(module):

#     if module not in MODULE_CONTENT_TYPES:
#         return None

#     app_label, model = MODULE_CONTENT_TYPES[module]

#     try:
#         return ContentType.objects.get(
#             app_label=app_label,
#             model=model
#         )
#     except ContentType.DoesNotExist:
#         return None


# # =====================================================
# # GET ALL ACTIVITIES FOR A MODULE RECORD
# #
# # GET /api/activities/lead/4/
# # GET /api/activities/deal/4/
# # GET /api/activities/company/4/
# # GET /api/activities/ticket/4/
# # =====================================================

# class ActivityTimelineView(APIView):

#     permission_classes = [IsAuthenticated]

#     def get(self, request, module, module_id):

#         # ==============================================
#         # FIND CONTENT TYPE
#         # ==============================================

#         content_type = get_content_type(module)

#         if not content_type:
#             return Response(
#                 {
#                     "error": "Invalid module."
#                 },
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # ==============================================
#         # GET ACTIVITIES
#         # ==============================================

#         activities = (
#             Activity.objects
#             .filter(
#                 content_type=content_type,
#                 object_id=module_id
#             )
#             .select_related(
#                 "created_by",
#                 "content_type"
#             )
#             .order_by("-created_at")
#         )

#         # ==============================================
#         # SERIALIZE
#         # ==============================================

#         serializer = ActivitySerializer(
#             activities,
#             many=True
#         )

#         return Response(serializer.data)


# # =====================================================
# # GET ACTIVITIES OF ONE TYPE
# #
# # GET /api/activities/lead/4/note/
# # GET /api/activities/lead/4/call/
# # GET /api/activities/lead/4/task/
# # GET /api/activities/lead/4/meeting/
# # GET /api/activities/lead/4/email/
# # =====================================================

# class ActivityTypeDetailView(APIView):

#     permission_classes = [IsAuthenticated]

#     VALID_ACTIVITY_TYPES = [
#         "note",
#         "call",
#         "task",
#         "meeting",
#         "email",
#     ]

#     def get(
#         self,
#         request,
#         module,
#         module_id,
#         activity_type
#     ):

#         # ==============================================
#         # VALIDATE ACTIVITY TYPE
#         # ==============================================

#         if activity_type not in self.VALID_ACTIVITY_TYPES:

#             return Response(
#                 {
#                     "error": "Invalid activity type."
#                 },
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # ==============================================
#         # FIND CONTENT TYPE
#         # ==============================================

#         content_type = get_content_type(module)

#         if not content_type:

#             return Response(
#                 {
#                     "error": "Invalid module."
#                 },
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # ==============================================
#         # GET ACTIVITIES
#         # ==============================================

#         activities = (
#             Activity.objects
#             .filter(
#                 content_type=content_type,
#                 object_id=module_id,
#                 activity_type=activity_type
#             )
#             .select_related(
#                 "created_by",
#                 "content_type"
#             )
#             .order_by("-created_at")
#         )

#         # ==============================================
#         # SERIALIZE
#         # ==============================================

#         serializer = ActivitySerializer(
#             activities,
#             many=True
#         )

#         return Response(
#             {
#                 "module": module,
#                 "module_id": module_id,
#                 "activity_type": activity_type,
#                 "activities": serializer.data
#             }
#         )


from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework.permissions import IsAuthenticated 
from rest_framework import status 
 
from django.contrib.contenttypes.models import ContentType 
 
from .models import Activity 
from .serializers import ActivitySerializer 
 
 
# ===================================================== 
# MODULE → CONTENT TYPE 
# ===================================================== 
 
MODULE_CONTENT_TYPES = { 
    "lead": ("leads", "lead"), 
    "deal": ("deals", "deal"), 
    "company": ("companies", "company"), 
    "ticket": ("tickets", "ticket"), 
} 
 
 
def get_content_type(module): 
 
    if module not in MODULE_CONTENT_TYPES: 
        return None 
 
    app_label, model = MODULE_CONTENT_TYPES[module] 
 
    try: 
        return ContentType.objects.get( 
            app_label=app_label, 
            model=model 
        ) 
    except ContentType.DoesNotExist: 
        return None 
 
 
# ===================================================== 
# GET ALL ACTIVITIES FOR A MODULE RECORD 
# 
# GET /api/activities/lead/4/ 
# GET /api/activities/deal/4/ 
# ===================================================== 
 
class ActivityTimelineView(APIView): 
 
    permission_classes = [IsAuthenticated] 
 
    def get(self, request, module, module_id): 
 
        content_type = get_content_type(module) 
 
        if not content_type: 
 
            return Response( 
                { 
                    "error": "Invalid module." 
                }, 
                status=status.HTTP_400_BAD_REQUEST 
            ) 
 
        activities = ( 
            Activity.objects 
            .filter( 
                content_type=content_type, 
                object_id=module_id 
            ) 
            .select_related("created_by", "content_type") 
            .order_by("-created_at") 
        ) 
 
        serializer = ActivitySerializer( 
            activities, 
            many=True 
        ) 
 
        return Response(serializer.data) 
 
 
# ===================================================== 
# GET ACTIVITIES OF ONE TYPE 
# 
# GET /api/activities/lead/4/note/ 
# GET /api/activities/deal/4/meeting/ 
# ===================================================== 
 
class ActivityTypeDetailView(APIView): 
 
    permission_classes = [IsAuthenticated] 
 
    VALID_ACTIVITY_TYPES = [ 
        "note", 
        "call", 
        "task", 
        "meeting", 
        "email", 
    ] 
 
    def get( 
        self, 
        request, 
        module, 
        module_id, 
        activity_type 
    ): 
 
        # ============================================== 
        # VALIDATE ACTIVITY TYPE 
        # ============================================== 
 
        if activity_type not in self.VALID_ACTIVITY_TYPES: 
 
            return Response( 
                { 
                    "error": "Invalid activity type." 
                }, 
                status=status.HTTP_400_BAD_REQUEST 
            ) 
 
        # ============================================== 
        # FIND CONTENT TYPE 
        # ============================================== 
 
        content_type = get_content_type(module) 
 
        if not content_type: 
 
            return Response( 
                { 
                    "error": "Invalid module." 
                }, 
                status=status.HTTP_400_BAD_REQUEST 
            ) 
 
        # ============================================== 
        # GET ACTIVITIES 
        # ============================================== 
 
        activities = ( 
            Activity.objects 
            .filter( 
                content_type=content_type, 
                object_id=module_id, 
                activity_type=activity_type 
            ) 
            .select_related( 
                "created_by", 
                "content_type" 
            ) 
            .order_by("-created_at") 
        ) 
 
        # ============================================== 
        # SERIALIZE 
        # ============================================== 
 
        serializer = ActivitySerializer( 
            activities, 
            many=True 
        ) 
 
        return Response({ 
            "module": module, 
            "module_id": module_id, 
            "activity_type": activity_type, 
            "activities": serializer.data 
        }) 