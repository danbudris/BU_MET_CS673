from comm import views
from django.conf.urls import patterns, url, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'rooms', views.RoomViewSet)
router.register(r'messages', views.MessageViewSet)
router.register(r'messagedata', views.MessageDataViewSet)
router.register(r'roomuser', views.UserRoomViewSet)

urlpatterns = patterns('',
    url(r'^api/', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', include('comm.urls')),
)

