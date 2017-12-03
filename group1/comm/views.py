import django_filters
from django.shortcuts import render
from django.http import HttpResponse
from comm.models import User, Room, Message, UserRoom, IndvRoom, IndvMessage, UserVisit
from rest_framework import viewsets, generics, filters
from comm.serializers import UserSerializer, RoomSerializer, MessageSerializer, MessageDataSerializer, UserRoomSerializer, UserRoomDataSerializer, IndvRommSerializer, IndvMessageSerializer, UserVisitSerializer
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework import status
import random


# Return the main chat room
@login_required(login_url='/signin')
def index(request):
    context = {'user': request.user}
    return render(request, 'comm/index.html', context)


@login_required(login_url='/signin')
def videochat(request):
        context = {'user': request.user}
        return render(request, 'comm/videochat.html', context)


@login_required(login_url='/signin')
def help(request):
	context = {'user': request.user}
	return render(request, 'comm/help.html', context)

@login_required(login_url='/signin')
def room(request,roomID):
	context = {'roomID' : roomID}
	return render(request,'comm/test.html',context)


# Django REST framework classes...
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class IndvRoomViewSet(viewsets.ModelViewSet):
	queryset = IndvRoom.objects.all()
	serializer_class = IndvRommSerializer
	#filter_class = IndvRoomFilter
	def get(self, request, format=None):
		users = IndvRoom.objects.all()
		serializer = IndvRommSerializer(users, many=True)
		return Response(serializer.data)

	def post(self, request, format=None):
		serializer = IndvRommSerializer(data=request.data)
		creator_id=int(request.data.get("create_user", ""))
		users=request.data.get("users", "")
		second_user=request.data.get("second_user", "")
		creator_user=User.objects.get(id=creator_id)
		indvroom=IndvRoom()
		indvroom.users=users
		indvroom.create_user=creator_user
		indvroom.second_user=second_user
		indvroom.save()
		#if serializer.is_valid():
			#serializer.save()
			#return Response(serializer.data, status=status.HTTP_201_CREATED)
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	def delete(self, request, pk, format=None):
		user = self.get_object(pk)
		user.delete()
        #return Response(status=status.HTTP_204_NO_CONTENT)

class IndvMessageViewSet(viewsets.ModelViewSet):
	queryset = IndvMessage.objects.all()
	serializer_class = IndvMessageSerializer
	#filter_class = IndvRoomFilter
	def get(self, request, format=None):
		users = IndvMessage.objects.all()
		serializer = IndvMessageSerializer(users, many=True)
		return Response(serializer.data)

	def post(self, request, format=None):
		serializer = IndvMessageSerializer(data=request.data)
		send_user_id=int(request.data.get("send_user", ""))
		indv_room=int(request.data.get("indv_room", ""))
		text=request.data.get("text", "")
		send_user=User.objects.get(id=send_user_id)
		indv_message=IndvMessage()
		indv_message.text=text
		indv_message.send_user=send_user
		indv_message.indv_room=indv_room
		indv_message.save()
	def put(self, request):
		id = int(request.data.get("id", "0"))
		text = request.data.get("text", "0")
		indv_message = IndvMessage.objects.get(pk=id)
		indv_message.text = text
		indv_message.save()

	def delete(self, request):
		id = int(request.data.get("id", "0"))
		indv_message = IndvMessage.objects.get(pk=id)
		indv_message.delete()
        #return Response(status=status.HTTP_204_NO_CONTENT)

class RoomViewSet(viewsets.ModelViewSet):
	queryset = Room.objects.all()
	serializer_class = RoomSerializer
	def put(self, request):
		id = int(request.data.get("id", "0"))
		name = request.data.get("name", "0")
		room = Room.objects.get(pk=id)
		room.name = name
		room.save()
	def delete(self, request):
		id = int(request.data.get("id", "0"))
		room = Room.objects.get(pk=id)
		room.delete()
    
class UserVisitViewSet(viewsets.ModelViewSet):
	queryset = UserVisit.objects.all()
	serializer_class = UserVisitSerializer

	def get(self, request, format=None):
		users = UserVisit.objects.all()
		serializer = UserVisitSerializer(users, many=True)
		return Response(serializer.data)
	def post(self, request, format=None):
		serializer = UserVisitSerializer(data=request.data)
		user = int(request.data.get("user", ""))
		userID = User.objects.get(id=user)
		user_visit = UserVisit()
		user_visit.user = userID
		user_visit.save()

	def put(self, request):
		id = int(request.data.get("id", "0"))
		#user = request.data.get("user", "0")
		user_visit = UserVisit.objects.get(pk=id)
		#user_visit.user = user
		user_visit.save()

# Filters the Message model based on user and room, 
# url: 127.0.0.1:8000/api/messages/? (user=id | room=id | user=id & room=id)
class MessageFilter(django_filters.FilterSet):
    user = django_filters.NumberFilter(name="user__id")
    room = django_filters.NumberFilter(name="room__id")

    class Meta:
        model = Message
        fields = ['user', 'room']


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('id')
    serializer_class = MessageSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = MessageFilter

    def put(self, request):
        id = int(request.data.get("id", "0"))
        text = request.data.get("text", "0")
        message = Message.objects.get(pk=id)
        message.text = text
        message.save()

    def delete(self, request):
        id = int(request.data.get("id", "0"))
        message = Message.objects.get(pk=id)
        message.delete()


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


class MessageSearchSet(viewsets.ReadOnlyModelViewSet):
    queryset = Message.objects.all().order_by('time')
    serializer_class = MessageDataSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('text', 'time')
