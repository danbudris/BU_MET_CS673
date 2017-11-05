from comm.models import User, Room, Message, UserRoom, IndvRoom, IndvMessage
from rest_framework import routers, serializers, viewsets, filters

# Get list of online users
# Get last 100 messages

class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'username', 'email', 'last_login')

class RoomSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Room
		fields = ('id', 'name', 'creator', 'description', 'public')
class IndvRommSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = IndvRoom
		fields = ('id', 'users', 'create_user', 'second_user')

class IndvMessageSerializer(serializers.HyperlinkedModelSerializer):
	#indv_room=IndvRommSerializer()
	#indv_room = serializers.HyperlinkedIdentityField(view_name="api:indv_room-detail")
	class Meta:
		model = IndvMessage
		fields = ('id', 'text', 'send_user', 'indv_room')

class MessageSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Message
		fields = ('id', 'text', 'time', 'at_message', 'room', 'user')

class UserRoomSerializer(serializers.HyperlinkedModelSerializer):
       class Meta:
                model = UserRoom
                fields = ('user', 'room')

class MessageDataSerializer(serializers.HyperlinkedModelSerializer):
	# This serializer will serialize all of the messages in the message model 
	# and all of the data associated with those messages.  The data from
	# the models User and Room will be displayed.
	room = RoomSerializer()
	user = UserSerializer()
	class Meta:
		model = Message
		fields = ('text', 'time', 'at_message', 'room', 'user')

class UserRoomDataSerializer(serializers.HyperlinkedModelSerializer):
	user = UserSerializer()       
	room = RoomSerializer()	
	class Meta:
                model = UserRoom
                fields = ('user', 'room')

# class PaginatedMessageSerializer(serializers.PaginationSerializer):
# 	class Meta:
# 		object_serializer_class = MessageSerializer
