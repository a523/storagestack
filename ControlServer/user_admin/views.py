from django.contrib.auth import models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from user_admin.serializers import UserSerializer


class Users(APIView):
    def get(self, request):
        """获取所有用户列表"""
        users = models.User.objects.defer('password').all()
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

    queryset = models.User.objects.all()
    serializer_class = UserSerializer
