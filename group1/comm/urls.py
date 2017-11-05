from django.conf.urls import patterns, url, include
from comm import views
from requirements.views import users

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^toolbar/changepasswd', users.changepasswd),
    url(r'^toolbar/userprofile', users.userprofile),
    url(r'^videochat/', views.videochat, name='videochat'),
)
