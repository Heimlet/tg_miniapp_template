from rest_framework.permissions import BasePermission

from users_app.models import User, Profile


class IsUserProfileOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, User):
            return obj == request.user
        elif isinstance(obj, Profile):
            return obj.user == request.user
        else:
            return False
