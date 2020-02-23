from django.contrib.auth import get_user_model
from rest_framework import serializers
from user_admin.models import ActionPermission

User = get_user_model()


class ActionPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActionPermission
        fields = ('app', 'codename', 'desc')
        read_only_fields = ('app', 'codename', 'desc')


class UserSerializer(serializers.ModelSerializer):
    action_permissions = ActionPermissionSerializer(many=True, required=False)

    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('is_superuser', 'last_login')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        action_permissions = validated_data.pop('action_permissions',  None)
        groups = validated_data.pop('groups', None)
        validated_data.pop('user_permissions', None)  # 目前不需要用到user_permissions
        user = User.objects.create_user(**validated_data)
        # TODO add action_permissions when create user
        return user

    def update(self, instance, validated_data):
        password = validated_data.get('password')
        if password:
            instance.set_password(password)

        instance.username = validated_data.get('username', instance.get_username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        groups = validated_data.get('groups')

        if groups:
            instance.groups = groups
        permiss = validated_data.get('user_permissions')
        if permiss:
            instance.user_permissions = permiss

        instance.save()

        return instance
