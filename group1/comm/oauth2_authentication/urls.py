from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns(
    '',
    url(r'filedownload/(?P<file_id>[\w-]+)', views.file_download, name='download'),
    url(r'oauth2callback/filedownload', views.callback_download, name='callback_download'),
)