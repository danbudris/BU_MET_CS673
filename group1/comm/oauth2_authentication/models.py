from django.db import models
from django.contrib.auth.models import User
from oauth2client.contrib.django_util.models import CredentialsField


class CredentialsModel(models.Model):
    id = models.ForeignKey(User, primary_key=True)
    credential = CredentialsField()
