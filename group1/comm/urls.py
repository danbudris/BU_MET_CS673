from django.conf.urls import patterns, url, include
from comm import views
from requirements.views import users

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^oauth2/', include('comm.oauth2_authentication.urls', namespace="oauth2")),
    url(r'^changepasswd', users.changepasswd),
    url(r'^userprofile', users.userprofile),
    url(r'^videochat/', views.videochat, name='videochat'),
)
