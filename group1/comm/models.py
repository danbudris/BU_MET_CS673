from django.db import models
from django.contrib.auth.models import User

# Need to add user relationship for second iteration
class Room(models.Model):

	def __repr__(self):
		return 'Room: %s' % self.name

	def __str__(self):
		return self.name

	name = models.CharField(max_length=100)
	creator = models.ForeignKey(User)
	description = models.CharField(max_length=500)
	public = models.BooleanField(default=True)
	#users = models.ManyToManyField(User)

class Message(models.Model):
	"""
	Encapsulates a message sent by a user.
	"""
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

from django.db.models.signals import post_save
from django.dispatch import receiver

#Delete oldest message when room has reached 5000 messages
@receiver(post_save, sender=Message)
def delete_oldest(sender, instance, **kwargs):
	curroom = instance.room
	queryset = Message.objects.defer('text').filter(room = curroom)
	count = queryset.count()
	if (count > 5000):
		oldest = queryset[:count-5000]
		for message in oldest:
			message.delete()


from django.db.models.signals import pre_save
@receiver(pre_save, sender=Message)
def prevent_maxChar(sender, instance, **kwargs):
	message = instance.text
	if len(message)>1050:
		sys.exit()
