import logging
from rest_framework import permissions
from django.contrib.auth import get_user_model

logger = logging.getLogger('control_server')
User = get_user_model()


class ActionPermission(permissions.BasePermission):
    """
    Global permission check for action (rest ful api url and method).
    """

    def has_permission(self, request, view):
        method = request.method.lower()
        try:
            method_func = getattr(view, method)
        except AttributeError as e:
            return True   # 忽略权限检查
        if not hasattr(method_func, 'permission'):
            return True
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


class UserModifyPermission(permissions.BasePermission):
    """这个是检查登录用户对已有用户进行修改编辑，有没有权限的检查
    权限高的用户组才可以对低权限用户做出修改
    不允许删除超级用户
    禁止对超级用户做任何修改，对超级用户的修改通过其他接口
    """
    message = 'Only high-level users can make changes to low-level users'

    def has_permission(self, request, view):
        method = request.method
        if method in permissions.SAFE_METHODS:
            return True
        else:
            try:
                uid = view.kwargs['pk']
                target_user = User.objects.get(id=uid)
                if request.user.is_superuser:
                    if target_user.is_superuser and method == "DELETE":
                        return False
                    else:
                        return True
                elif request.user.is_staff:
                    if target_user.is_superuser or target_user.is_staff:
                        return False
                    else:
                        return True
                else:
                    return False
            except (User.DoesNotExist, User.MultipleObjectsReturned) as e:
                logger.warning('A error in the permission check will be judged to be unprivileged')
                logger.warning(e)
                return True  # 获取实例失败， 忽略权限检查
