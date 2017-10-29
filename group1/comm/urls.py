from django.conf.urls import patterns, url, include
from comm import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^oauth2/', include('comm.oauth2_authentication.urls', namespace="oauth2")),
)
