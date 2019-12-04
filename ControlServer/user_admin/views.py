from django.contrib.auth import models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from user_admin.serializers import UserSerializer


class Users(APIView):
    def get(self, request):
        """获取所有用户列表"""
        # 验证数据
        users = models.User.objects.defer('password').all()
        users = UserSerializer(users, many=True).data
        return Response(data=users, status=status.HTTP_200_OK)

