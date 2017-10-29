import os
import httplib2
from oauth2client.contrib import xsrfutil
from oauth2client.client import flow_from_clientsecrets
from oauth2client.contrib.django_util.storage import DjangoORMStorage
from googleapiclient.discovery import build
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.contrib.sites.models import get_current_site
from .models import CredentialsModel, FlowModel

CLIENT_SECRETS = os.path.join(
    os.path.dirname(__file__), 'client_secrets.json')


def get_accounts_ids(service):
    accounts = service.management().accounts().list().execute()
    ids = []
    if accounts.get('items'):
        for account in accounts['items']:
            ids.append(account['id'])
    return ids


@login_required
def index(request):
    # use the first redirect_uri if you are developing your app
    # locally, and the second in production
    redirect_uri = 'http://localhost:8000/communication/oauth2/oauth2callback'
    # redirect_uri = "https://%s%s" % (
    #    get_current_site(request).domain, reverse("oauth2:return"))
    flow = flow_from_clientsecrets(
        CLIENT_SECRETS,
        scope='https://www.googleapis.com/auth/drive',
        redirect_uri=redirect_uri
    )
    user = request.user
    storage = DjangoORMStorage(CredentialsModel, 'id', user, 'credential')
    credential = storage.get()
    if credential is None or credential.invalid is True:
        flow.params['state'] = xsrfutil.generate_token(
            settings.SECRET_KEY, user)
        authorize_url = flow.step1_get_authorize_url()
        f = FlowModel(id=user, flow=flow)
        f.save()
        return HttpResponseRedirect(authorize_url)
    else:
        http = httplib2.Http()
        http = credential.authorize(http)
        service = build('drive', 'v3', http=http)
        ids = get_accounts_ids(service)
        return render(
            request, 'oauth2_authentication/main.html', {'ids': ids})


@login_required
def auth_return(request):
    user = request.user
    if not xsrfutil.validate_token(
            settings.SECRET_KEY, request.REQUEST['state'], user):
        return HttpResponseBadRequest()
    flow = FlowModel.objects.get(id=user).flow
    credential = flow.step2_exchange(request.REQUEST)
    storage = DjangoORMStorage(CredentialsModel, 'id', user, 'credential')
    storage.put(credential)
    return HttpResponseRedirect("/oauth2")
