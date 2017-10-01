import django_filters
from django.shortcuts import render
from django.http import HttpResponse
from comm.models import User, Room, Message, UserRoom
from rest_framework import viewsets, generics
from comm.serializers import UserSerializer, RoomSerializer, MessageSerializer, MessageDataSerializer, UserRoomSerializer, UserRoomDataSerializer
import random

# Return the main chat room
def index(request):
	context = {'user': random.choice(User.objects.all())}
	return render(request, 'comm/index.html', context)

## Django REST framework classes...
class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer

class RoomViewSet(viewsets.ModelViewSet):
	queryset = Room.objects.all()
	serializer_class = RoomSerializer

class MessageFilter(django_filters.FilterSet):
	user = django_filters.CharFilter(name="user__name")
	room = django_filters.CharFilter(name="room__name")
	class Meta:
		model = Message
		fields = ['user', 'room']

class MessageViewSet(viewsets.ModelViewSet):
	queryset = Message.objects.all().order_by('time')
	serializer_class = MessageSerializer
	filter_class = MessageFilter

class MessageDataViewSet(viewsets.ReadOnlyModelViewSet):
	# This viewset will show all of the messages in the message model 
	# and all of the data associated with those messages.  The data from
	# the models User and Room will be displayed.
	queryset = Message.objects.all().order_by('time')
	serializer_class = MessageDataSerializer
	filter_class = MessageFilter

class UserRoomFilter(django_filters.FilterSet):
	user = django_filters.CharFilter(name="user__name")
	room = django_filters.CharFilter(name="room__name")
	class Meta:
		model = UserRoom
		fields = ['user', 'room']

class UserRoomViewSet(viewsets.ModelViewSet):
	queryset = UserRoom.objects.all()
	serializer_class = UserRoomSerializer
	filter_class = UserRoomFilter

class UserRoomDataViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = UserRoom.objects.all()
	serializer_class = UserRoomDataSerializer
	filter_class = UserRoomFilter
