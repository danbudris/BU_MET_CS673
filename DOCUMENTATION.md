# Documentation
This document describes how to use the Django admindocs documentation suite to view this app's documentation.

## Prerequisites
* The application is installed and configured according to the (README.md) README document.
* The virtualenv is active and you are able to navigate to the site in a dev environment.
* You have installed docutils, found here: http://docutils.sourceforge.net/

## Viewing Documentation
* Navigate to your local version of the site and append /admin to the URL, for example: ```http://127.0.0.1:8000/admin```
* Sign in with a super-user account
* Click on the "documentation" link in the upper right-hand corner of the screen.

## Writing Documentation
* Documentation should be written using docstrings, like in the following example:
```
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
```

* More on using admindocs can be found by viewing the documentation here: https://docs.djangoproject.com/en/1.10/ref/contrib/admin/admindocs/#module-django.contrib.admindocs