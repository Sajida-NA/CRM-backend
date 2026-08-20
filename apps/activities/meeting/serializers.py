# from rest_framework import serializers

# from .models import Meeting


# class MeetingSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Meeting

#         fields = [
#             "id",
#             "title",
#             "owner",
#             "start_date",
#             "start_time",
#             "end_time",
#             "attendees",
#             "location",
#             "reminder",
#             "note",
#             "created_at",
#             "updated_at",
#         ]

#         read_only_fields = [
#             "id",
#             "created_at",
#             "updated_at",
#         ]


from rest_framework import serializers

from .models import Meeting


# =========================================================
# CREATE / UPDATE
# =========================================================

class MeetingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Meeting

        fields = [
            "id",
            "activity_type",
            "module",
            "title",
            "owner",
            "start_date",
            "start_time",
            "end_time",
            "attendees",
            "location",
            "reminder",
            "note",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


# =========================================================
# RESPONSE
# =========================================================

class MeetingResponseSerializer(serializers.ModelSerializer):

    owner = serializers.SerializerMethodField()
    attendees = serializers.SerializerMethodField()

    class Meta:
        model = Meeting

        fields = [
            "id",
            "activity_type",
            "module",
            "title",
            "owner",
            "start_date",
            "start_time",
            "end_time",
            "attendees",
            "location",
            "reminder",
            "note",
            "created_at",
            "updated_at",
        ]

    def get_owner(self, obj):

        if not obj.owner:
            return None

        name = (
            f"{obj.owner.first_name} "
            f"{obj.owner.last_name}"
        ).strip()

        return name or obj.owner.email

    def get_attendees(self, obj):

        return [
            (
                f"{user.first_name} "
                f"{user.last_name}"
            ).strip() or user.email
            for user in obj.attendees.all()
        ]