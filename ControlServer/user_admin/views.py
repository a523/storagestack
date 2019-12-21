from functools import wraps
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from user_admin.serializers import *

User = get_user_model()


class Users(APIView):
    def get(self, request):
        """获取所有用户列表"""
        users = User.objects.defer('password').all()
        users = UserSerializer(users, many=True).data
        return Response(data=users, status=status.HTTP_200_OK)

    def post(self, request):
        """创建新用户， 不可以是超级用户， 可以是管理员， 超级用户只允许通过命令行创建"""
        user_serial = UserSerializer(data=request.data)
        if user_serial.is_valid(raise_exception=True):
            new_user = user_serial.save()
            new_user = UserSerializer(new_user).data
            return Response(data=new_user, status=status.HTTP_201_CREATED)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


def permission_label(codename, desc=None):
    """具体某一个操作的权限定义和检验"""

    def decorator(func):
        # 定义权限
        permission = {"codename": codename}
        if desc:
            permission["desc"] = desc
        func.permission = permission

        @wraps(func)
        def wrap(*args, **kwargs):
            return func(*args, **kwargs)

        return wrap

    return decorator


class UserSelf(APIView):
    def get(self, request):
        """获取登录用户自己的信息"""
        user = request.user
        user_dict = UserSerializer(user).data
        act_permiss = user.get_all_action_permissions()
        all_action_permissions = ActionPermissionSerializer(act_permiss, many=True).data
        user_dict['all_action_permissions'] = all_action_permissions
        return Response(user_dict)
