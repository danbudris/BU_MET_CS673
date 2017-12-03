// Express and SocketIO boilerplate
var app = require('express')();
var morgan = require('morgan');
var http = require('http').Server(app);
var io = require('socket.io')(http);
var Client = require('node-rest-client').Client;
var os = require('os');
var util = require('util');
var _ = require('lodash');
var multer = require('multer');
var fs = require('fs-extra');
var crypto = require('crypto');
var url = require('url');
var path = require('path');

app.use(morgan('combined'));

// Add CORS headers to all express requests
app.all('/*', function(req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "X-Requested-With");
    next();
});


// sets path of home directory according to the OS
var homedir = (process.platform === 'win32') ? process.env.HOMEPATH : process.env.HOME;
// just for file upload
var done = false;
app.use(multer({
        'dest': '../../comm/static/uploads/',
        onFileUploadStart: function(file) {
            if (testNameValidation(file.originalname)) {
                console.log(file.originalname + ' is starting...');
            } else {
                console.log('File name is invalid');
                return false;
            }
        },
        onFileUploadComplete: function(file) {
                console.log(file.fieldname + ' uploaded to ' + file.path);
                done = true;
        }
}));

function testNameValidation(text) {
    var format = /[ !@#$%^&*()+\-=\[\]{};':"\\|,<>\/?]/;
    if (text.trim() == null || text.trim() == "" || format.test(text) == true)  {
        return false;
    } else {
        return true;
    }
}

app.post('/upload', function(req,res){
    var pathname = url.parse(req.headers.referer).pathname;
    if (done==true) {
        var hash = crypto.randomBytes(20).toString('hex');
		var directory =  path.resolve(process.cwd() + '/../../comm/static/uploads/');
        directory = directory + "/";
        fs.mkdirs(path.join(directory, hash), function(err) {
            if (err) {
                console.log(err);
            } else {
                var final_path = path.join(hash, req.files.fileUpload.originalname);
                fs.rename(req.files.fileUpload.path, directory + final_path);
                res.send('static/uploads/' + final_path);
            }
        });
    } else {
        res.send('Error');
    }
});

var client = new Client();

// We should stash the username (ID?) of everyone connected to the global namespace here
var users = [];

var global_namespace = io.of('/');

global_namespace.on('connection', function(socket){
        var user;
        socket.on('user', function(msg) { 
                console.log(msg);
                user = msg.username;
                users.push(user);
                global_namespace.emit('user', {'username': user, 'action': 'connected' });
                console.log( util.format('%s connected', user) );
        });
        socket.on('disconnect', function(){
                users.pop(user);
                console.log( util.format('%s disconnected', user) );
                global_namespace.emit('user', {'username': user, 'action': 'disconnected' });
        });
        socket.on('room', function(room){
                console.log('new room: '  + room.name);
                rooms.save(room.name, room.creator_id, room.description, room.public);
        });
        socket.on('updateroom', function(room){
                rooms.update(room);
                global_namespace.emit('updateroom', room);
        });
        socket.on('deleteroom', function(room) {
                rooms.delete(room);
                global_namespace.emit('deleteroom', room);
        });

        socket.on('userroom', function(userroom) {
                userroom.save(userroom);
        });

        socket.on('editmsg', function(msg) {
            messages.update(msg);
        });
        socket.on('deletemsg', function(msgid) {
            messages.delete(msgid);
        });
});


// Make a REST call to get the currently connected users

app.get('/users', function(req,res){
        res.header
        res.send(_.unique(users));
});

var room_url = 'http://localhost:8000/api/rooms/?format=json';

namespaces = {};

function add_new_namespace(room) {
  namespaces[room.id] = io.of(util.format('/%s', room.id))
    .on('connection', function(socket) {
        console.log(util.format('conncted to room %s', room.id ));
        socket.on('msg',function(msg){
            console.log(util.format('message from %s: %s', msg.username, msg.value));
            messages.save(room.id, util.format('%s: %s', msg.username, msg.value), msg.user_id);
        });
        socket.on('disconnect',function(){
            console.log(util.format('someone disconnected from %s', room.id ));
        });
    });
}

client.get(room_url,function(data,response){
  data.forEach(function(room){
    add_new_namespace(room);
  });
});

var messages = {
        'save': function(room_id, message, user_id) {
                message_template = {
                        data: {
                                'at_message': false,
                                'room': util.format('http://localhost:8000/api/rooms/%s/', room_id),
                                'user': util.format('http://localhost:8000/api/users/%s/', user_id),
                                'text': message 
                        },
                        headers: { 'Content-Type': 'application/json' }
                };
                client.post('http://localhost:8000/api/messages/', message_template, function(data,response) {
                        namespaces[room_id].emit('msg', data);
                        console.log( util.format('(%s) Room %s : "%s"', response.statusCode, room_id, message) );
                });
        },
        'update': function(msg) {
                message_template = {
                        data: {
                                'id': msg.id,
                                'text': msg.text
                        },
                        headers: { 'Content-Type': 'application/json' }
                };
                client.put('http://localhost:8000/api/messages/', message_template, function(data,response) {
                        global_namespace.emit('editmsg', msg);
                        console.log( util.format('(%s) Message %s editted to: "%s"', response.statusCode, msg.id, msg.text) );
                });
        },
        'delete': function(msgid) {
                message_template = {
                        data: {
                            'id': msgid
                        },
                        headers: { 'Content-Type': 'application/json' }
                };
                client.delete('http://localhost:8000/api/messages/', message_template, function(data,response) {
                        global_namespace.emit('deletemsg', msgid);
                        console.log( util.format('(%s) Message %s deleted', response.statusCode, msgid) );
                });
        }
};

var rooms = {
        'save': function(name, creator_id, desc, pub) {
                room_template = {
                        data: {
                                'name': name,
                                'creator': util.format('http://localhost:8000/api/users/%s/', creator_id),
                                'description': desc,
                                'public': pub,
                        },
                        headers: { 'Content-Type': 'application/json' }
                };
                client.post('http://localhost:8000/api/rooms/', room_template, function(data,response) {
                        console.log( util.format('(%s) Room %s created by user "%s" with room id %s', response.statusCode, name, creator_id, data.id) );

                        add_new_namespace(data);
                        global_namespace.emit('room', data);
                        userroom.save({room: data.id, user: creator_id});
                });
        },
        'update': function(room) {
                room_template = {
                        data: {
                                'id': room.id,
                                'name': room.name,
                                'creator': room.creator,
                                'description': room.description,
                                'public': room.public,
                        },
                        headers: { 'Content-Type': 'application/json' }
                };
                client.put('http://localhost:8000/api/rooms/', room_template, function(data,response) {
                        console.log( util.format('(%s) Room %s updated to "%s"', response.statusCode, room.id, room.name) );
                });
        },
        'delete': function(room) {
                room_template = {
                        data: {
                                'id': room.id,
                        },
                        headers: { 'Content-Type': 'application/json' }
                };
                client.delete('http://localhost:8000/api/rooms/', room_template, function(data,response) {
                        console.log( util.format('(%s) Room %s was deleted', response.statusCode, room.id) );
                });
        }
};

var userroom = {    
    'save': function(userroom_data) {        
        userroom_template = {                        
            data: {           
                'user': util.format('http://localhost:8000/api/users/%s/', userroom_data.user),
                'room': util.format('http://localhost:8000/api/rooms/%s/', userroom_data.room)
            },                        
            headers: { 'Content-Type': 'application/json' }                
        };                
        client.post('http://localhost:8000/api/roomuser/', userroom_template, function(data,response) {                        
            console.log(util.format('(%s) User %s has joined Room "%s"', response.statusCode, data.user, data.room) );
        });                
    }
};


var msg_endpoint = 'http://127.0.0.1:8000/api/messages/';

var message_template = {
        "data": {
                "at_message": false,
                "room": "http://localhost:8000/api/rooms/1/",
        "user": "http://localhost:8000/api/users/1/"
        },
        "headers": { "Content-Type": "application/json" }
};

var channels = {};
var sockets = {};

// WebSocket stuff
io.on('connection', function(socket) {
        socket.on('msg', function(msg) {
                io.emit('msg', msg);
                message_template.data.text = msg;
                client.post(msg_endpoint, message_template, function(data,response) { console.log(msg) });
        });

	    console.log("channels "+channels)
    socket.channels={};
    sockets[socket.id] = socket;

    console.log("["+ socket.id + "] connection accepted");

    socket.on('disconnect', function () {
        for (var channel in socket.channels) {
            part(channel);
            console.log("socket channels" + channel);
        }
        console.log("["+ socket.id + "] disconnected");
        delete sockets[socket.id];
    });


    console.log("A user connected");

    socket.on('join', function (config) {
        console.log("["+ socket.id + "] join ", config);
        var channel = config.channel;
        var userdata = config.userdata;

        if (channel in socket.channels) {
            console.log("["+ socket.id + "] ERROR: already joined ", channel);
            return;
        }

        if (!(channel in channels)) {
            channels[channel] = {};
        }

        for (id in channels[channel]) {
            console.log("channels "+channels);
            console.log("channel_id "+id);
            channels[channel][id].emit('addPeer', {'peer_id': socket.id, 'should_create_offer': false});
            socket.emit('addPeer', {'peer_id': id, 'should_create_offer': true});
            console.log("emitting Add PEER");
        }

        channels[channel][socket.id] = socket;
        socket.channels[channel] = channel;
    });

    function part(channel) {
        console.log("["+ socket.id + "] part ");

        if (!(channel in socket.channels)) {
            console.log("["+ socket.id + "] ERROR: not in ", channel);
            return;
        }

        delete socket.channels[channel];
        delete channels[channel][socket.id];

        for (id in channels[channel]) {
            channels[channel][id].emit('removePeer', {'peer_id': socket.id});
            socket.emit('removePeer', {'peer_id': id});
        }
    }
    socket.on('part', part);

    socket.on('relayICECandidate', function(config) {
        var peer_id = config.peer_id;
        var ice_candidate = config.ice_candidate;
        console.log("["+ socket.id + "] relaying ICE candidate to [" + peer_id + "] ", ice_candidate);

        if (peer_id in sockets) {
            sockets[peer_id].emit('iceCandidate', {'peer_id': socket.id, 'ice_candidate': ice_candidate});
        }
    });

    socket.on('relaySessionDescription', function(config) {
        var peer_id = config.peer_id;
        var session_description = config.session_description;
        console.log("["+ socket.id + "] relaying session description to [" + peer_id + "] ", session_description);

        if (peer_id in sockets) {
            sockets[peer_id].emit('sessionDescription', {'peer_id': socket.id, 'session_description': session_description});
        }
    });


   socket.on('disconnect', function () {
       console.log("An user disconnected");
   })
});

// Start the server
http.listen(3000, function(){
        console.log('Starting NodeJS server');
        console.log('listening on 3000');
});
