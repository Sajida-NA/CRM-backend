from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .models import User



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)
    role = serializers.ChoiceField(
      choices=[
        ("Admin", "Admin"),
        ("User", "User"),
      ],
      write_only=True,
    )

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
            "role",
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

        role = validated_data.pop("role")

        password = validated_data.pop("password")

        user = User.objects.create_user(
        password=password,
        **validated_data,
        )

        group = Group.objects.get(name=role)

        user.groups.add(group)

        return user

class AddUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)

    role = serializers.ChoiceField(
        choices=[
            ("Admin", "Admin"),
            ("User", "User"),
        ],
        write_only=True,
    )

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
            "role",
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

        role = validated_data.pop("role")

        password = validated_data.pop("password")

        user = User.objects.create_user(
        password=password,
        **validated_data,
        )

        group = Group.objects.get(name=role)

        user.groups.add(group)

        return user



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(
            username=email,
            password=password,
        )

        if not user:
            raise serializers.ValidationError(
                "Invalid email or password."
            )

        attrs["user"] = user
        return attrs

class ProfileSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "company_name",
            "industry_type",
            "country",
            "role",
        )
    def get_role(self, obj):
        group = obj.groups.first()
        return group.name if group else None

class UserListSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "company_name",
            "industry_type",
            "country",
            "role",
            "is_active",
        )

    def get_role(self, obj):
        group = obj.groups.first()
        return group.name if group else None

class UpdateUserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        choices=[
            ("Admin", "Admin"),
            ("User", "User"),
        ],
        write_only=True,
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "company_name",
            "industry_type",
            "country",
            "role",
        )

    def update(self, instance, validated_data):
        role = validated_data.pop("role")

        for attr, value in validated_data.items():
           setattr(instance, attr, value)

        instance.save()

        group = Group.objects.get(name=role)

        instance.groups.clear()
        
        instance.groups.add(group)

        return instance

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            raise serializers.ValidationError("Invalid or expired token.")

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
    )
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8,
        style={"input_type": "password"},
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
    )

    def validate(self, attrs):
        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": "Passwords do not match."}
            )
        return attrs


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={"input_type": "password"},
    )
    confirm_password = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
    )

    def validate(self, attrs):
        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": "Passwords do not match."}
            )
        return attrs
    