from rest_framework import permissions


class ActionPermission(permissions.BasePermission):
    """
    Global permission check for action (rest ful api url and method).
    """

    def has_permission(self, request, view):
        method = request.method.lower()
        view_permission = getattr(view, method).permission
        if not view_permission:
            return True
        else:
            user_permissions = request.user.get_all_action_permissions
            if view_permission in user_permissions:
                return True
            else:
                return False
