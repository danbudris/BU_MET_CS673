from django.db import models
from django.contrib.auth.models import User
from base import ProjMgmtBase


class Project(ProjMgmtBase):
    # todo add stories

    users = models.ManyToManyField(User, through='UserAssociation')

    def __str__(self):
        return self.title

    def description_as_list(self):
        return self.description.split('\n')

    class Meta:
        permissions = (
            ("own_project", "Can own and create projects"),
        )

        app_label = 'requirements'
