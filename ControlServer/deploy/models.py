from django.db import models


class Nodes(models.Model):
    ip = models.GenericIPAddressField(unique=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
