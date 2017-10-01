from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from requirements.views import users
from requirements.views import home
from requirements import req_urls
from rest_framework.routers import DefaultRouter
from comm import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'rooms', views.RoomViewSet)
router.register(r'messagedata', views.MessageDataViewSet, 'messagedata')
router.register(r'messagesearch', views.MessageSearchSet, 'messagesearch')
router.register(r'messages', views.MessageViewSet, 'message')
router.register(r'roomuserdata', views.UserRoomDataViewSet, 'roomuserdata')
router.register(r'roomuser', views.UserRoomViewSet, 'roomuser')



urlpatterns = patterns('',
                        url(r'^signin', users.signin),
                        url(r'^signout', users.signout),
                        url(r'^signup', users.signup),
                        url(r'^req/', include(req_urls)),
                        url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
                        url(r'^admin/',include(admin.site.urls)),
                        url(r'^$', home.home_page),
                        url(r'^communication/',include('comm.urls')),
                        url(r'^issue_tracker/',include('issue_tracker.urls')),
                        url(r'^admin/doc/',include('django.contrib.admindocs.urls')),
                        url(r'^api/', include(router.urls)),
                        

                       # url(r'^admin/', include(admin.site.urls)),
                      )
