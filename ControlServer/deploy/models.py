from django.db import models


class Nodes(models.Model):
    ip = models.GenericIPAddressField()
    create_time = models.DateTimeField(auto_created=True)
