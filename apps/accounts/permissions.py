from rest_framework.permissions import BasePermission


class IsAdminGroup(BasePermission):
    """
    Allows access only to users in the Admin group.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.groups.filter(name="Admin").exists()
        )