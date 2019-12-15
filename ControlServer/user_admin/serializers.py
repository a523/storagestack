from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('is_superuser', 'last_login')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        # TODO 修改的时候可以不提供username
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
