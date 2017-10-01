import requests
import unittest
import commands
import json
from socketIO_client import SocketIO, BaseNamespace
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

class TestChatAPI(StaticLiveServerTestCase):

	def test_get_users(self):
		res = requests.get('http://127.0.0.1:8000/api/users/?format=json')
		users = res.json()
		self.assertTrue(res.status_code == 200)
		self.assertTrue( len(users) > 0 )

	def test_get_messages(self):
		res = requests.get('http://127.0.0.1:8000//api/messages/?format=json')
		messages = res.json()
		self.assertTrue(res.status_code == 200)

	def test_get_rooms(self):
		res = requests.get('http://127.0.0.1:8000/api/rooms/?format=json')
		rooms = res.json()
		self.assertTrue(res.status_code == 200)
		self.assertTrue( len(rooms) > 0 )



class TestSocketIO(unittest.TestCase):

	def test_global_namespace_REST_endpoint(self):
		res = requests.get('http://127.0.0.1:8000/users')
		self.assertTrue( res.status_code == 200 )


if __name__ == '__main__':
	unittest.main()