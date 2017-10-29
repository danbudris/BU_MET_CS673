from django.db import models
from django.contrib.auth.models import User
from oauth2client.contrib.django_util.models import CredentialsField
from oauth2client.client import flow_from_clientsecrets


class FlowModel(models.Model):
    id = models.ForeignKey(User, primary_key=True)
    flow = flow_from_clientsecrets('comm/oauth2_authentication/client_secrets.json',
                                   scope='https://www.googleapis.com/auth/drive',
                                   redirect_uri='http://localhost:8000/oauth2/oauth2callback')


class CredentialsModel(models.Model):
    id = models.ForeignKey(User, primary_key=True)
    credential = CredentialsField()
