from rest_framework import permissions


class ActionPermission(permissions.BasePermission):
    """
    Global permission check for action (rest ful api url and method).
    """

    def has_permission(self, request, view):
        method = request.method.lower()
        view_permission = getattr(view, method).permission
        view_permission_key = (view.__module__.split('.')[0],) + (view_permission['codename'],)
        if not view_permission:
            return True
        else:
            user_permissions = request.user.get_all_action_permissions()
            user_permissions_key = {p.natural_key() for p in user_permissions}
            if view_permission_key in user_permissions_key:
                return True
            else:
                return False
