from django.core.management.base import BaseCommand, CommandError
from user_admin import urls

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self):
        try:
            for url in urls.urlpatterns:
                url.lookup_str
        except Poll.DoesNotExist:
            raise CommandError('Poll "%s" does not exist' % poll_id)

        poll.opened = False
        poll.save()

        self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))