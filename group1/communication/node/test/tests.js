var assert = require("assert");
var test = require('unit.js');
var supertest = require('supertest');

var Client = require('node-rest-client').Client;
var client = new Client();

describe('API tests:', function(){

	var api_test = supertest('http://localhost');

	describe('rooms', function(){
		it('should return at least one room object', function(err, done) {
			client.get('http://localhost/api/rooms/?format=json', function(data,response){
				if (data.length === 0) { throw err };
			});
			done();
		});
	});
});

		// it('should return at least one room object', function(done) {
		// 	api_test.get('/api/roomskkk/?format=json').expect(201, function(err){ return err });
		// 	done();
		// });

	// 	var temp_room;

	// 	it('can create new room', function(){
	// 		var room_url = 'http://localhost/api/rooms/';
	// 		message_template = {
	// 			data: {
	// 				'name': 'Test Room',
	// 				'description': 'Test Description',
	// 				'public': true 
	// 			},
	// 			headers: { 'Content-Type': 'application/json' }
	// 		};
	// 		client.post(room_url, message_template, function(data,response){
	// 			temp_room = data;
	// 		});
	// 		assert.equal(temp_room.statusCode, 201);
	// 	});


	// Python code
	//  for msg in Room.objects.filter(name = 'Test Room'): msg.delete()

	// 	// it('can delete that room', function(){
	// 	// 	var room_url = 'http://localhost/api/rooms/?format=json';
	// 	// 	client.get(room_url,function(data,response){
	// 	// 		// assert.notEqual(data.length,0);
	// 	// 	});
	// 	// });

	// });

	// describe('messages', function(){

	// 	it('should be able to get messages', function(){
	// 		var user_url = 'http://localhost/api/messages/?format=json';
	// 		client.get(user_url, function(data,response){
	// 			assert.Equal(response.statusCode,200);
	// 		});
	// 	});

	// });

	// describe('users', function(){

	// 	it('should return at least one user', function(){
	// 		var user_url = 'http://localhost/api/users/?format=json';
	// 		client.get(user_url,function(data,response){
	// 			assert.notEqual(data.length,0);
	// 		});
	// 	});

	// });
