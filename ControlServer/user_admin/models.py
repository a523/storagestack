from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group as AuthGroup


class ActionPermission(models.Model):
    """
    事件权限模型
    """
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'
    METHOD = [
        (GET, "get"),
        (POST, "post"),
        (PUT, "put"),
        (DELETE, "delete"),
    ]
    app = models.CharField(_('app'), max_length=100)
    codename = models.CharField(_('codename'), max_length=100)
    view = models.CharField(_('view'), max_length=100)
    method = models.CharField(_('method'), choices=METHOD, max_length=8)
    desc = models.CharField(_('desc'), max_length=255)

    class Meta:
        verbose_name = _('action_permission')
        verbose_name_plural = _('action_permission')
        unique_together = (('app', 'codename'),)
        ordering = ('app', 'view', 'codename')

    def __str__(self):
        return '%s | %s' % (self.app, self.codename)

    def natural_key(self):
        return (self.app,) + (self.codename,)


class User(AbstractUser):
    action_permissions = models.ManyToManyField(ActionPermission, verbose_name=_('action_permissions'), blank=True)

    def get_user_action_permissions(self):
        if not self.is_active or self.is_anonymous:
            return set()
        if self.is_superuser:
            return ActionPermission.objects.all()
        return self.action_permissions.all()

    def get_group_action_permissions(self):
        if not self.is_active or self.is_anonymous:
            return set()
        if self.is_superuser:
            return ActionPermission.objects.all()
        user_groups_field = self._meta.get_field('groups')
        user_groups_query = 'groups__%s' % user_groups_field.related_query_name()
        return ActionPermission.objects.filter(**{user_groups_query: self})

    def get_all_action_permissions(self):
        if not self.is_active or self.is_anonymous:
            return set()
        return {
            *self.get_user_action_permissions(),
            *self.get_group_action_permissions(),
        }


class Group(AuthGroup):
    action_permissions = models.ManyToManyField(
        ActionPermission,
        verbose_name=_('action_permissions'),
        blank=True,
    )
