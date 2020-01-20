from types import FunctionType
from django.core.management.base import BaseCommand, CommandError
from django.utils.module_loading import import_module, import_string
from django.conf import settings
from user_admin.models import ActionPermission

installed_apps = settings.INSTALLED_APPS


class Command(BaseCommand):
    help = 'collect permissions to write database'
    methods = ('get', 'post', 'put', 'delete')

    def handle(self,  *args, **options):
        try:
            for app in installed_apps:
                if app.startswith('django.'):
                    # 忽略自带app
                    continue
                urls = import_module(app+'.urls')
                for url in urls.urlpatterns:
                    view_full_path = url.lookup_str
                    view_name = view_full_path.split('.')[-1]
                    view = import_string(view_full_path)
                    if type(view) is FunctionType:
                        pass
                        # 目前只支持类方法上加权限
                    else:
                        for method in Command.methods:
                            try:
                                method_fun = getattr(view, method)
                                permission = method_fun.permission
                            except AttributeError:
                                continue
                            permission['app'] = app
                            permission['method'] = method
                            permission['view'] = view_name
                            ActionPermission.objects.update_or_create(**permission)
        except Exception as e:
            raise CommandError(str(e))

        self.stdout.write(self.style.SUCCESS('Successfully collect permissions to database'))
