import requests
import unittest
import commands
import json
from socketIO_client import SocketIO, BaseNamespace

### General
class TestInfrastructure(unittest.TestCase):

	output = commands.getoutput('ps -A')

	def test_cdn(self):
		self.assertTrue(requests.get('https://cdnjs.cloudflare.com').status_code == 200)

	def test_gunicorn_running(self):
		self.assertTrue('gunicorn' in self.output)

	def test_node_running(self):
		self.assertTrue('node' in self.output)

	def test_nginx_running(self):
		self.assertTrue('nginx' in self.output)

	def test_reverse_proxy(self):
		website_text = requests.get('http://localhost').text
		title = 'Communication tool'
		self.assertTrue(title in website_text)

	def test_python_dependencies(self):

		pip_output = commands.getoutput('pip freeze').split('\n')
		available = [line.strip() for line in pip_output if '==' in line]
		requirements_file = [line.strip() for line in open('/home/cs673/Comm-Tool/requirements.txt')]

		for line in requirements_file:
			self.assertTrue(line in available)

	def test_node_dependencies(self):
		pass

class TestAPI(unittest.TestCase):
	
	def test_get_users(self):
		res = requests.get('http://localhost/api/users/?format=json')
		users = res.json()
		self.assertTrue(res.status_code == 200)
		self.assertTrue( len(users) > 0 ) 

	def test_get_messages(self):
		res = requests.get('http://localhost/api/messages/?format=json')
		messages = res.json()
		self.assertTrue(res.status_code == 200)

	def test_get_rooms(self):
		res = requests.get('http://localhost/api/rooms/?format=json')
		rooms = res.json()
		self.assertTrue(res.status_code == 200)
		self.assertTrue( len(rooms) > 0 ) 

	def test_create_public_room(self):
		room_data = {
			'name': 'test_room',
			'description': 'testing room API',
			'public': True
		}
		pass

	def test_create_private_room(self):
		pass

	def test_file_upload(self):
		pass

class TestSocketIO(unittest.TestCase):

	def test_global_namespace_REST_endpoint(self):
		res = requests.get('http://localhost:3000/users')
		self.assertTrue( res.status_code == 200 )

	def test_global_namespace_connect(self):
		with SocketIO('localhost', 3000) as socket:
			global_ns = socket.define(BaseNamespace, '/')
			global_ns.emit('user', {'username':'test', 'action':'connect'})

			res = requests.get('http://localhost:3000/users')			
			self.assertTrue('test' in res.json() )


class SeleniumTests(unittest.TestCase):

	def test_something(self):
		pass

if __name__ == '__main__':
	unittest.main()