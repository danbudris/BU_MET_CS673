from django.db import models
from django.contrib.auth.models import User


class ProjMgmtBase(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=1024, blank=True, default='')

    # Last Updated Time, automatically updated every time an instance is saved
    last_updated = models.DateTimeField(auto_now=True, null=True)

    # todo add status as a Field.choices

    def __str__(self):
        return self.title

    class Meta:
        abstract = True
