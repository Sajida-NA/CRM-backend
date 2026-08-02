from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "company_name",
            "industry_type",
            "country",
            "password",
            "confirm_password",
        ]
    
    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": "Passwords do not match."}
            )
        return attrs

    
    def create(self, validated_data):
        validated_data.pop("confirm_password")
        password = validated_data.pop("password")

       
        return User.objects.create_user(
        password=password,
        **validated_data,
    )