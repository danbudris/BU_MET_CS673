from django.db import models
from django.contrib.auth.models import User

# Need to add user relationship for second iteration
class Room(models.Model):

	def __repr__(self):
		return 'Room: %s' % self.name

	def __str__(self):
		return self.name

	name = models.CharField(max_length=100)
	description = models.CharField(max_length=500)
	public = models.BooleanField(default=True)
	#users = models.ManyToManyField(User)

class Message(models.Model):

	def __str__(self):
		return '%s - %s' % (self.user, self.text)

	text = models.TextField()
	time = models.DateTimeField(auto_now=True)
	room = models.ForeignKey(Room)
	user = models.ForeignKey(User)
	at_message = models.BooleanField(default=False)

class UserRoom(models.Model):
	user = models.ForeignKey(User)
	room = models.ForeignKey(Room)

	class Meta:
		unique_together = ('user', 'room')
