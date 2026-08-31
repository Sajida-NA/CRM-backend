# from django.contrib.auth import get_user_model
# from django.contrib.contenttypes.models import ContentType

# from rest_framework import serializers

# from .models import Meeting
# from apps.activities.activity.models import Activity


# User = get_user_model()


# # =========================================================
# # CREATE / UPDATE SERIALIZER
# # =========================================================

# class MeetingSerializer(serializers.ModelSerializer):

#     # -----------------------------------------
#     # INPUT ONLY
#     # -----------------------------------------

#     sender_id = serializers.IntegerField(
#         write_only=True,
#         required=False
#     )

#     module = serializers.CharField(
#         write_only=True,
#         required=False
#     )

#     module_id = serializers.IntegerField(
#         write_only=True,
#         required=False
#     )

#     class Meta:

#         model = Meeting

#         fields = [
#             "id",

#             # Input
#             "sender_id",
#             "module",
#             "module_id",

#             # Meeting
#             "title",
#             "owner",
#             "start_date",
#             "start_time",
#             "end_time",
#             "attendees",
#             "location",
#             "reminder",
#             "note",

#             # Timestamps
#             "created_at",
#             "updated_at",
#         ]

#         read_only_fields = [
#             "id",
#             "owner",
#             "created_at",
#             "updated_at",
#         ]

#     # =====================================================
#     # VALIDATE
#     # =====================================================

#     def validate(self, attrs):

#         # For CREATE
#         if self.instance is None:

#             sender_id = attrs.pop("sender_id")
#             module = attrs.pop("module").lower()
#             module_id = attrs.pop("module_id")

#             # -----------------------------------------
#             # Validate sender
#             # -----------------------------------------

#             try:
#                 sender = User.objects.get(id=sender_id)

#             except User.DoesNotExist:
#                 raise serializers.ValidationError({
#                     "sender_id": "Sender does not exist."
#                 })

#             # -----------------------------------------
#             # Allowed modules
#             # -----------------------------------------

#             MODULE_MAP = {

#                 "lead": (
#                     "leads",
#                     "lead"
#                 ),

#                 "deal": (
#                     "deals",
#                     "deal"
#                 ),

#                 "company": (
#                     "companies",
#                     "company"
#                 ),

#                 "ticket": (
#                     "tickets",
#                     "ticket"
#                 ),
#             }

#             if module not in MODULE_MAP:

#                 raise serializers.ValidationError({
#                     "module": (
#                         "Invalid module. "
#                         "Allowed modules: "
#                         "lead, deal, company, ticket."
#                     )
#                 })

#             app_label, model_name = MODULE_MAP[module]

#             # -----------------------------------------
#             # Get ContentType
#             # -----------------------------------------

#             try:

#                 content_type = ContentType.objects.get(
#                     app_label=app_label,
#                     model=model_name
#                 )

#             except ContentType.DoesNotExist:

#                 raise serializers.ValidationError({
#                     "module": (
#                         f"{module} module does not exist."
#                     )
#                 })

#             # -----------------------------------------
#             # Validate CRM object
#             # -----------------------------------------

#             model_class = content_type.model_class()

#             try:

#                 related_object = model_class.objects.get(
#                     id=module_id
#                 )

#             except model_class.DoesNotExist:

#                 raise serializers.ValidationError({
#                     "module_id": (
#                         f"{module} with id "
#                         f"{module_id} does not exist."
#                     )
#                 })

#             # Store internal values
#             attrs["_sender"] = sender
#             attrs["content_type"] = content_type
#             attrs["object_id"] = module_id

#         return attrs

#     # =====================================================
#     # CREATE
#     # =====================================================

#     def create(self, validated_data):

#         # Get sender
#         sender = validated_data.pop("_sender")

#         # Remove attendees before creating Meeting
#         attendees = validated_data.pop(
#             "attendees",
#             []
#         )

#         # Get module connection
#         content_type = validated_data.get(
#             "content_type"
#         )

#         object_id = validated_data.get(
#             "object_id"
#         )

#         # -----------------------------------------
#         # CREATE CENTRAL ACTIVITY
#         # -----------------------------------------

#         activity = Activity.objects.create(
#             activity_type="meeting",
#             created_by=sender,
#             content_type=content_type,
#             object_id=object_id
#         )

#         # -----------------------------------------
#         # CREATE MEETING
#         # -----------------------------------------

#         meeting = Meeting.objects.create(
#             activity=activity,
#             owner=sender,
#             **validated_data
#         )

#         # -----------------------------------------
#         # ADD ATTENDEES
#         # -----------------------------------------

#         if attendees:
#             meeting.attendees.set(attendees)

#         return meeting

#     # =====================================================
#     # UPDATE
#     # =====================================================

#     def update(self, instance, validated_data):

#         # Remove input-only fields if sent accidentally
#         validated_data.pop("sender_id", None)
#         validated_data.pop("module", None)
#         validated_data.pop("module_id", None)

#         # Handle attendees
#         attendees = validated_data.pop(
#             "attendees",
#             None
#         )

#         # Update normal fields
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)

#         instance.save()

#         # Update attendees only if provided
#         if attendees is not None:
#             instance.attendees.set(attendees)

#         return instance


# # =========================================================
# # RESPONSE SERIALIZER
# # =========================================================

# class MeetingResponseSerializer(
#     serializers.ModelSerializer
# ):

#     created_by = serializers.SerializerMethodField()

#     module = serializers.SerializerMethodField()

#     lead = serializers.SerializerMethodField()

#     attendees = serializers.SerializerMethodField()

#     class Meta:

#         model = Meeting

#         fields = [
#             "id",
#             "created_by",
#             "module",
#             "lead",
#             "title",
#             "start_date",
#             "start_time",
#             "end_time",
#             "attendees",
#             "location",
#             "reminder",
#             "note",
#         ]

#     # =====================================================
#     # CREATED BY
#     # =====================================================

#     def get_created_by(self, obj):

#         if not obj.owner:
#             return None

#         return {
#             "id": obj.owner.id,
#             "name": (
#                 obj.owner.get_full_name()
#                 or obj.owner.email
#             )
#         }

#     # =====================================================
#     # MODULE
#     # =====================================================

#     def get_module(self, obj):

#         if not obj.content_type:
#             return None

#         return obj.content_type.model

#     # =====================================================
#     # RELATED OBJECT
#     # =====================================================

#     def get_lead(self, obj):

#         related_object = obj.related_object

#         if not related_object:
#             return None

#         model_name = obj.content_type.model

#         # -----------------------------------------
#         # LEAD
#         # -----------------------------------------

#         if model_name == "lead":

#             return {
#                 "id": related_object.id,
#                 "name": (
#                     f"{related_object.first_name} "
#                     f"{related_object.last_name}"
#                 ).strip()
#             }

#         # -----------------------------------------
#         # DEAL
#         # -----------------------------------------

#         if model_name == "deal":

#             lead = getattr(
#                 related_object,
#                 "associated_lead",
#                 None
#             )

#             if lead:

#                 return {
#                     "id": lead.id,
#                     "name": (
#                         f"{lead.first_name} "
#                         f"{lead.last_name}"
#                     ).strip()
#                 }

#             return {
#                 "id": related_object.id,
#                 "name": getattr(
#                     related_object,
#                     "deal_name",
#                     str(related_object)
#                 )
#             }

#         # -----------------------------------------
#         # COMPANY
#         # -----------------------------------------

#         if model_name == "company":

#             return {
#                 "id": related_object.id,
#                 "name": getattr(
#                     related_object,
#                     "name",
#                     str(related_object)
#                 )
#             }

#         # -----------------------------------------
#         # TICKET
#         # -----------------------------------------

#         if model_name == "ticket":

#             return {
#                 "id": related_object.id,
#                 "name": getattr(
#                     related_object,
#                     "name",
#                     str(related_object)
#                 )
#             }

#         return None

#     # =====================================================
#     # ATTENDEES
#     # =====================================================

#     def get_attendees(self, obj):

#         return [
#             {
#                 "id": user.id,
#                 "name": (
#                     user.get_full_name()
#                     or user.email
#                 )
#             }
#             for user in obj.attendees.all()
#         ]



# from django.contrib.auth import get_user_model
# from django.contrib.contenttypes.models import ContentType

# from rest_framework import serializers

# from .models import Meeting
# from apps.activities.activity.models import Activity


# User = get_user_model()


# # =========================================================
# # CREATE / UPDATE SERIALIZER
# # =========================================================

# class MeetingSerializer(serializers.ModelSerializer):

#     # =====================================================
#     # INPUT ONLY
#     # =====================================================

#     sender_id = serializers.IntegerField(
#         write_only=True,
#         required=True
#     )

#     module = serializers.CharField(
#         write_only=True,
#         required=True
#     )

#     module_id = serializers.IntegerField(
#         write_only=True,
#         required=True
#     )

#     class Meta:

#         model = Meeting

#         fields = [
#             "id",

#             # Input
#             "sender_id",
#             "module",
#             "module_id",

#             # Meeting
#             "title",
#             "owner",
#             "start_date",
#             "start_time",
#             "end_time",
#             "attendees",
#             "location",
#             "reminder",
#             "note",

#             # Timestamps
#             "created_at",
#             "updated_at",
#         ]

#         read_only_fields = [
#             "id",
#             "owner",
#             "created_at",
#             "updated_at",
#         ]

#     # =====================================================
#     # VALIDATE
#     # =====================================================

#     def validate(self, attrs):

#         # Only required during CREATE
#         if self.instance is None:

#             sender_id = attrs.pop("sender_id")
#             module = attrs.pop("module").lower()
#             module_id = attrs.pop("module_id")

#             # -------------------------------------------------
#             # VALIDATE SENDER
#             # -------------------------------------------------

#             try:

#                 sender = User.objects.get(
#                     id=sender_id
#                 )

#             except User.DoesNotExist:

#                 raise serializers.ValidationError({
#                     "sender_id": "Sender does not exist."
#                 })

#             # -------------------------------------------------
#             # ALLOWED MODULES
#             # -------------------------------------------------

#             MODULE_MAP = {

#                 "lead": (
#                     "leads",
#                     "lead"
#                 ),

#                 "deal": (
#                     "deals",
#                     "deal"
#                 ),

#                 "company": (
#                     "companies",
#                     "company"
#                 ),

#                 "ticket": (
#                     "tickets",
#                     "ticket"
#                 ),
#             }

#             if module not in MODULE_MAP:

#                 raise serializers.ValidationError({
#                     "module": (
#                         "Invalid module. "
#                         "Allowed modules: "
#                         "lead, deal, company, ticket."
#                     )
#                 })

#             app_label, model_name = MODULE_MAP[module]

#             # -------------------------------------------------
#             # GET CONTENT TYPE
#             # -------------------------------------------------

#             try:

#                 content_type = ContentType.objects.get(
#                     app_label=app_label,
#                     model=model_name
#                 )

#             except ContentType.DoesNotExist:

#                 raise serializers.ValidationError({
#                     "module": (
#                         f"{module} module does not exist."
#                     )
#                 })

#             # -------------------------------------------------
#             # GET RELATED MODEL
#             # -------------------------------------------------

#             model_class = content_type.model_class()

#             if model_class is None:

#                 raise serializers.ValidationError({
#                     "module": (
#                         f"Unable to find model for {module}."
#                     )
#                 })

#             # -------------------------------------------------
#             # VALIDATE CRM OBJECT
#             # -------------------------------------------------

#             try:

#                 related_object = model_class.objects.get(
#                     id=module_id
#                 )

#             except model_class.DoesNotExist:

#                 raise serializers.ValidationError({
#                     "module_id": (
#                         f"{module} with id "
#                         f"{module_id} does not exist."
#                     )
#                 })

#             # -------------------------------------------------
#             # STORE INTERNAL VALUES
#             # -------------------------------------------------

#             attrs["_sender"] = sender

#             attrs["content_type"] = content_type

#             attrs["object_id"] = module_id

#         return attrs

#     # =====================================================
#     # CREATE
#     # =====================================================

#     def create(self, validated_data):

#         # -------------------------------------------------
#         # GET SENDER
#         # -------------------------------------------------

#         sender = validated_data.pop(
#             "_sender"
#         )

#         # -------------------------------------------------
#         # GET ATTENDEES
#         # -------------------------------------------------

#         attendees = validated_data.pop(
#             "attendees",
#             []
#         )

#         # -------------------------------------------------
#         # GET MODULE DATA
#         # -------------------------------------------------

#         content_type = validated_data.pop(
#             "content_type"
#         )

#         object_id = validated_data.pop(
#             "object_id"
#         )

#         # -------------------------------------------------
#         # CREATE CENTRAL ACTIVITY
#         # -------------------------------------------------

#         activity = Activity.objects.create(
#             activity_type="meeting",
#             created_by=sender,
#             content_type=content_type,
#             object_id=object_id
#         )

#         # -------------------------------------------------
#         # CREATE MEETING
#         # -------------------------------------------------

#         meeting = Meeting.objects.create(
#             activity=activity,
#             owner=sender,
#             content_type=content_type,
#             object_id=object_id,
#             **validated_data
#         )

#         # -------------------------------------------------
#         # ADD MULTIPLE ATTENDEES
#         # -------------------------------------------------

#         if attendees:

#             meeting.attendees.set(
#                 attendees
#             )

#         return meeting

#     # =====================================================
#     # UPDATE
#     # =====================================================

#     def update(self, instance, validated_data):

#         # -------------------------------------------------
#         # REMOVE INPUT-ONLY FIELDS
#         # -------------------------------------------------

#         validated_data.pop(
#             "sender_id",
#             None
#         )

#         validated_data.pop(
#             "module",
#             None
#         )

#         validated_data.pop(
#             "module_id",
#             None
#         )

#         # -------------------------------------------------
#         # HANDLE ATTENDEES
#         # -------------------------------------------------

#         attendees = validated_data.pop(
#             "attendees",
#             None
#         )

#         # -------------------------------------------------
#         # UPDATE NORMAL FIELDS
#         # -------------------------------------------------

#         for attr, value in validated_data.items():

#             setattr(
#                 instance,
#                 attr,
#                 value
#             )

#         instance.save()

#         # -------------------------------------------------
#         # UPDATE MULTIPLE ATTENDEES
#         # -------------------------------------------------

#         if attendees is not None:

#             instance.attendees.set(
#                 attendees
#             )

#         return instance


# # =========================================================
# # RESPONSE SERIALIZER
# # =========================================================

# class MeetingResponseSerializer(
#     serializers.ModelSerializer
# ):

#     created_by = serializers.SerializerMethodField()

#     module = serializers.SerializerMethodField()

#     lead = serializers.SerializerMethodField()

#     attendees = serializers.SerializerMethodField()

#     class Meta:

#         model = Meeting

#         fields = [
#             "id",
#             "created_by",
#             "module",
#             "lead",
#             "title",
#             "start_date",
#             "start_time",
#             "end_time",
#             "attendees",
#             "location",
#             "reminder",
#             "note",
#         ]

#     # =====================================================
#     # CREATED BY
#     # =====================================================

#     def get_created_by(self, obj):

#         if not obj.owner:
#             return None

#         return {
#             "id": obj.owner.id,

#             "name": (
#                 obj.owner.get_full_name()
#                 or obj.owner.email
#             )
#         }

#     # =====================================================
#     # MODULE
#     # =====================================================

#     def get_module(self, obj):

#         if not obj.content_type:
#             return None

#         return obj.content_type.model

#     # =====================================================
#     # RELATED OBJECT / LEAD
#     # =====================================================

#     def get_lead(self, obj):

#         related_object = obj.related_object

#         if not related_object:
#             return None

#         if not obj.content_type:
#             return None

#         model_name = obj.content_type.model

#         # -------------------------------------------------
#         # LEAD
#         # -------------------------------------------------

#         if model_name == "lead":

#             return {
#                 "id": related_object.id,

#                 "name": (
#                     f"{related_object.first_name} "
#                     f"{related_object.last_name}"
#                 ).strip()
#             }

#         # -------------------------------------------------
#         # DEAL
#         # -------------------------------------------------

#         if model_name == "deal":

#             lead = getattr(
#                 related_object,
#                 "associated_lead",
#                 None
#             )

#             if lead:

#                 return {
#                     "id": lead.id,

#                     "name": (
#                         f"{lead.first_name} "
#                         f"{lead.last_name}"
#                     ).strip()
#                 }

#             return {
#                 "id": related_object.id,

#                 "name": getattr(
#                     related_object,
#                     "deal_name",
#                     str(related_object)
#                 )
#             }

#         # -------------------------------------------------
#         # COMPANY
#         # -------------------------------------------------

#         if model_name == "company":

#             return {
#                 "id": related_object.id,

#                 "name": getattr(
#                     related_object,
#                     "name",
#                     str(related_object)
#                 )
#             }

#         # -------------------------------------------------
#         # TICKET
#         # -------------------------------------------------

#         if model_name == "ticket":

#             return {
#                 "id": related_object.id,

#                 "name": getattr(
#                     related_object,
#                     "name",
#                     str(related_object)
#                 )
#             }

#         return None

#     # =====================================================
#     # ATTENDEES
#     # =====================================================

#     def get_attendees(self, obj):

#         return [
#             {
#                 "id": user.id,

#                 "name": (
#                     user.get_full_name()
#                     or user.email
#                 )
#             }

#             for user in obj.attendees.all()
#         ]


from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from .models import Meeting
from apps.activities.activity.models import Activity


User = get_user_model()


# =========================================================
# CREATE / UPDATE SERIALIZER
# =========================================================

class MeetingSerializer(serializers.ModelSerializer):

    # =====================================================
    # INPUT ONLY
    # =====================================================

    sender_id = serializers.IntegerField(
        write_only=True,
        required=True
    )

    module = serializers.CharField(
        write_only=True,
        required=True
    )

    module_id = serializers.IntegerField(
        write_only=True,
        required=True
    )

    class Meta:

        model = Meeting

        fields = [
            "id",

            # Input
            "sender_id",
            "module",
            "module_id",

            # Meeting
            "title",
            "owner",
            "start_date",
            "start_time",
            "end_time",
            "attendees",
            "location",
            "reminder",
            "note",

            # Timestamps
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "owner",
            "created_at",
            "updated_at",
        ]

    # =====================================================
    # VALIDATE
    # =====================================================

    def validate(self, attrs):

        # -------------------------------------------------
        # CREATE ONLY
        # -------------------------------------------------

        if self.instance is None:

            sender_id = attrs.pop(
                "sender_id"
            )

            module = attrs.pop(
                "module"
            ).lower()

            module_id = attrs.pop(
                "module_id"
            )

            # -------------------------------------------------
            # VALIDATE SENDER
            # -------------------------------------------------

            try:

                sender = User.objects.get(
                    id=sender_id
                )

            except User.DoesNotExist:

                raise serializers.ValidationError({
                    "sender_id": "Sender does not exist."
                })

            # -------------------------------------------------
            # ALLOWED MODULES
            # -------------------------------------------------

            MODULE_MAP = {

                "lead": (
                    "leads",
                    "lead"
                ),

                "deal": (
                    "deals",
                    "deal"
                ),

                "company": (
                    "companies",
                    "company"
                ),

                "ticket": (
                    "tickets",
                    "ticket"
                ),
            }

            if module not in MODULE_MAP:

                raise serializers.ValidationError({
                    "module": (
                        "Invalid module. "
                        "Allowed modules: "
                        "lead, deal, company, ticket."
                    )
                })

            app_label, model_name = MODULE_MAP[module]

            # -------------------------------------------------
            # GET CONTENT TYPE
            # -------------------------------------------------

            try:

                content_type = ContentType.objects.get(
                    app_label=app_label,
                    model=model_name
                )

            except ContentType.DoesNotExist:

                raise serializers.ValidationError({
                    "module": (
                        f"{module} module does not exist."
                    )
                })

            # -------------------------------------------------
            # GET RELATED MODEL
            # -------------------------------------------------

            model_class = content_type.model_class()

            if model_class is None:

                raise serializers.ValidationError({
                    "module": (
                        f"Unable to find model for {module}."
                    )
                })

            # -------------------------------------------------
            # VALIDATE CRM OBJECT
            # -------------------------------------------------

            try:

                model_class.objects.get(
                    id=module_id
                )

            except model_class.DoesNotExist:

                raise serializers.ValidationError({
                    "module_id": (
                        f"{module} with id "
                        f"{module_id} does not exist."
                    )
                })

            # -------------------------------------------------
            # STORE INTERNAL VALUES
            # -------------------------------------------------

            attrs["_sender"] = sender

            attrs["_content_type"] = content_type

            attrs["_object_id"] = module_id

        return attrs

    # =====================================================
    # CREATE
    # =====================================================

    def create(self, validated_data):

        # -------------------------------------------------
        # GET SENDER
        # -------------------------------------------------

        sender = validated_data.pop(
            "_sender"
        )

        # -------------------------------------------------
        # GET ATTENDEES
        # -------------------------------------------------

        attendees = validated_data.pop(
            "attendees",
            []
        )

        # -------------------------------------------------
        # GET MODULE DATA
        # -------------------------------------------------

        content_type = validated_data.pop(
            "_content_type"
        )

        object_id = validated_data.pop(
            "_object_id"
        )

        # -------------------------------------------------
        # CREATE CENTRAL ACTIVITY
        # -------------------------------------------------

        activity = Activity.objects.create(
            activity_type="meeting",
            created_by=sender,
            content_type=content_type,
            object_id=object_id
        )

        # -------------------------------------------------
        # CREATE MEETING
        # -------------------------------------------------

        meeting = Meeting.objects.create(
            activity=activity,
            owner=sender,
            **validated_data
        )

        # -------------------------------------------------
        # ADD ATTENDEES
        # -------------------------------------------------

        if attendees:

            meeting.attendees.set(
                attendees
            )

        return meeting

    # =====================================================
    # UPDATE
    # =====================================================

    def update(self, instance, validated_data):

        # -------------------------------------------------
        # REMOVE INPUT-ONLY FIELDS
        # -------------------------------------------------

        validated_data.pop(
            "sender_id",
            None
        )

        validated_data.pop(
            "module",
            None
        )

        validated_data.pop(
            "module_id",
            None
        )

        validated_data.pop(
            "_sender",
            None
        )

        validated_data.pop(
            "_content_type",
            None
        )

        validated_data.pop(
            "_object_id",
            None
        )

        # -------------------------------------------------
        # HANDLE ATTENDEES
        # -------------------------------------------------

        attendees = validated_data.pop(
            "attendees",
            None
        )

        # -------------------------------------------------
        # UPDATE NORMAL FIELDS
        # -------------------------------------------------

        for attr, value in validated_data.items():

            setattr(
                instance,
                attr,
                value
            )

        instance.save()

        # -------------------------------------------------
        # UPDATE ATTENDEES
        # -------------------------------------------------

        if attendees is not None:

            instance.attendees.set(
                attendees
            )

        return instance


# =========================================================
# RESPONSE SERIALIZER
# =========================================================

class MeetingResponseSerializer(
    serializers.ModelSerializer
):

    created_by = serializers.SerializerMethodField()

    module = serializers.SerializerMethodField()

    lead = serializers.SerializerMethodField()

    attendees = serializers.SerializerMethodField()

    class Meta:

        model = Meeting

        fields = [
            "id",
            "created_by",
            "module",
            "lead",
            "title",
            "start_date",
            "start_time",
            "end_time",
            "attendees",
            "location",
            "reminder",
            "note",
        ]

    # =====================================================
    # CREATED BY
    # =====================================================

    def get_created_by(self, obj):

        if not obj.owner:
            return None

        return {
            "id": obj.owner.id,

            "name": (
                obj.owner.get_full_name()
                or obj.owner.email
            )
        }

    # =====================================================
    # MODULE
    # =====================================================

    def get_module(self, obj):

        if not obj.activity:
            return None

        content_type = obj.activity.content_type

        if not content_type:
            return None

        return content_type.model

    # =====================================================
    # RELATED OBJECT / LEAD
    # =====================================================

    def get_lead(self, obj):

        # -------------------------------------------------
        # GET ACTIVITY
        # -------------------------------------------------

        if not obj.activity:
            return None

        activity = obj.activity

        # -------------------------------------------------
        # GET CONTENT TYPE
        # -------------------------------------------------

        content_type = activity.content_type

        if not content_type:
            return None

        # -------------------------------------------------
        # GET OBJECT ID
        # -------------------------------------------------

        object_id = activity.object_id

        if not object_id:
            return None

        # -------------------------------------------------
        # GET RELATED OBJECT
        # -------------------------------------------------

        try:

            related_object = content_type.get_object_for_this_type(
                id=object_id
            )

        except content_type.model_class().DoesNotExist:

            return None

        if not related_object:
            return None

        model_name = content_type.model

        # =================================================
        # LEAD
        # =================================================

        if model_name == "lead":

            return {
                "id": related_object.id,

                "name": (
                    f"{getattr(related_object, 'first_name', '')} "
                    f"{getattr(related_object, 'last_name', '')}"
                ).strip()
            }

        # =================================================
        # DEAL
        # =================================================

        if model_name == "deal":

            lead = getattr(
                related_object,
                "associated_lead",
                None
            )

            if lead:

                return {
                    "id": lead.id,

                    "name": (
                        f"{getattr(lead, 'first_name', '')} "
                        f"{getattr(lead, 'last_name', '')}"
                    ).strip()
                }

            return {
                "id": related_object.id,

                "name": getattr(
                    related_object,
                    "deal_name",
                    str(related_object)
                )
            }

        # =================================================
        # COMPANY
        # =================================================

        if model_name == "company":

            return {
                "id": related_object.id,

                "name": getattr(
                    related_object,
                    "name",
                    str(related_object)
                )
            }

        # =================================================
        # TICKET
        # =================================================

        if model_name == "ticket":

            return {
                "id": related_object.id,

                "name": getattr(
                    related_object,
                    "name",
                    str(related_object)
                )
            }

        return None

    # =====================================================
    # ATTENDEES
    # =====================================================

    def get_attendees(self, obj):

        return [
            {
                "id": user.id,

                "name": (
                    user.get_full_name()
                    or user.email
                )
            }

            for user in obj.attendees.all()
        ]