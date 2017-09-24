from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
                       url(r'/^$',
                           'project_router.views.home_page',
                           name='home_page'),
                       )