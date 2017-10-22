from django.conf.urls import patterns, url, include
from comm import views
from requirements.views import users

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^changepasswd', users.changepasswd),
    url(r'^userprofile', users.userprofile),
)
