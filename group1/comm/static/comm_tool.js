String.prototype.splice = function( idx, rem, s ) {
    return (this.slice(0,idx) + s + this.slice(idx + Math.abs(rem)));
};

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function createteam(){
  $("#myModal").modal('show');
}

// EMOJI STUFF
function emoji_input(emoji_name) {
  $('input#text').val($('input#text').val()+emoji_name);
}

var emoji_image = {
  '::happy::': "<img src='/static/emoji/happy.jpg' style='width:20px;height:20px;'>",
  '::unhappy::':"<img src='/static/emoji/unhappy.jpg' style='width:20px;height:20px;'>",
  '::terrible::': "<img src='/static/emoji/terrible.jpg' style='width:20px;height:20px;'>",
  '::veryhappy::': "<img src='/static/emoji/veryhappy.jpg' style='width:20px;height:20px;'>",
  '::angry::': "<img src='/static/emoji/angry.jpg' style='width:20px;height:20px;'>",
  '::sweat::': "<img src='/static/emoji/sweat.jpg' style='width:20px;height:20px;'>",
  '::trick::': "<img src='/static/emoji/trick.jpg' style='width:20px;height:20px;'>",
  '::kiss::': "<img src='/static/emoji/kiss.jpg' style='width:20px;height:20px;'>",
  '::disappoint::': "<img src='/static/emoji/disappoint.jpg' style='width:20px;height:20px;'>",
  '::sick::': "<img src='/static/emoji/sick.jpg' style='width:20px;height:20px;'>",
  '::laughtear::': "<img src='/static/emoji/laughtear.jpg' style='width:20px;height:20px;'>",
  '::sadtear::': "<img src='/static/emoji/sadtear.jpg' style='width:20px;height:20px;'>",
  '::blink::': "<img src='/static/emoji/blink.jpg' style='width:20px;height:20px;'>",
  '::disdain::': "<img src='/static/emoji/disdain.jpg' style='width:20px;height:20px;'>",
  '::omg::': "<img src='/static/emoji/omg.jpg' style='width:20px;height:20px;'>",
  '::embarrased::': "<img src='/static/emoji/embarrased.jpg' style='width:20px;height:20px;'>",
  '::sillysmile::': "<img src='/static/emoji/sillysmile.jpg' style='width:20px;height:20px;'>",
  '::surprise::': "<img src='/static/emoji/surprise.jpg' style='width:20px;height:20px;'>",
  '::cry::': "<img src='/static/emoji/cry.jpg' style='width:20px;height:20px;'>",
  '::sleepy::': "<img src='/static/emoji/sleepy.jpg' style='width:20px;height:20px;'>",
  '::hearteye::': "<img src='/static/emoji/hearteye.jpg' style='width:20px;height:20px;'>",
  '::flush::': "<img src='/static/emoji/flush.jpg' style='width:20px;height:20px;'>",
  '::laughnoeye::': "<img src='/static/emoji/laughnoeye.jpg' style='width:20px;height:20px;'>",
  '::blue::': "<img src='/static/emoji/blue.jpg' style='width:20px;height:20px;'>",
  '::rat::': "<img src='/static/emoji/rat.jpg' style='width:20px;height:20px;'>",
  '::clrat::': "<img src='/static/emoji/clrat.jpg' style='width:20px;height:20px;'>",
  '::rabit::': "<img src='/static/emoji/rabit.jpg' style='width:20px;height:20px;'>",
  '::pig::': "<img src='/static/emoji/pig.jpg' style='width:20px;height:20px;'>",
  '::cat::': "<img src='/static/emoji/cat.jpg' style='width:20px;height:20px;'>",
  '::monkey::': "<img src='/static/emoji/monkey.jpg' style='width:20px;height:20px;'>",
}

//toggle the search bar
function search_show(){

  // search bar is hidden
  if ($('div#message_search').attr('class').indexOf('hidden') == -1) {
    $('div#message_search').addClass('hidden');
    $('div.messagecontent').css('padding-top', '70px');
  } 
  else {
    $('div#message_search').removeClass('hidden');
    $('div.messagecontent').css('padding-top', '130px');
  }
}

// global state variables
global_room_list = [];
global_user_list = [];

var server_host = window.location.hostname;
var base_url = 'http://' + server_host + ':3000/';
var global = io('http://' + server_host + ':3000');

global.emit('user', {
  'username': user,
  'action': 'connect',
});

global.on('room', function(room) { 
	add_new_room(room);
});

function createTeamFunc() {

    var new_team_name = $('input#teamname').val();
    var room_data = {
        'name': new_team_name,
        'description': 'test',
        'public': true
    };

    $.ajax({
        type: 'POST',
        url: 'http://' + server_host + '/api/rooms/',
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        data: room_data,
        success: function(room) {
            global.emit('room', room);
        },
    });

    $("#myModal").modal('hide');
}

global.on('user', function(user){

  var user_link = $('ul.user_list a').filter( function(link) { return $(this).text() === user.username }).parent();

  if (user.action == 'connected') {
    user_link.removeClass('disabled');
  } else if (user.action == 'disconnected') {
    user_link.addClass('disabled');
  }
  
});

sockets = {};
$.getJSON('http://' + server_host + '/api/rooms/',function(data){
  data.forEach(function(room){
    // add_socket(room);
  });
});

function add_socket(room) {
    var socket = io(base_url + room.id);
    socket.on('msg', function(msg) {
      if (room.id != visible_namespace()) {
        increment_badge(room.id);
      }
      add_message('<b>' + msg.username + '</b>: ' + msg.value, room.id);
    });
    sockets[room.id] = socket;
}

function increment_badge(room_id){
  var badge = $('div#room-list a').filter( function(){ return $(this).attr('id') === 'room-' + room_id } ).children().filter('.badge');
  var count = Number(badge.text());
  badge.text(count += 1);
}

function add_message(msg, target) {
  $('div#room-' + target).append(msg + '<br>');
  //add emoji to message content
  var emoji_string=Object.getOwnPropertyNames(emoji_image);
  if (msg.indexOf('::') != -1) {
    for(var i=0;i<emoji_string.length;i++){
      var each=emoji_string[i];
      var change=$('div#room-'+target).html();
      $('div#room-'+target).html(change.replace(each,emoji_image[each]));
    }
  }
}

function visible_namespace() {
  try {
    return Number($('div.messagecontent').filter(':visible').attr('id').replace('room-',''));
  } catch (TypeError) {
    return null;
  }
}

// Called when button is clicked
function display() {
  var message = {
    'username': user,
    'value': $('input#text').val(),
    'user_id': user_id
  }
  sockets[visible_namespace()].emit('msg', message);
  $('input#text').val('');
}

// Add a new message whenever the user presses the enter key
$(document).ready(function(){
        $("#text").keypress(function(e) {
            if(e.which == 13) {
                display();
            }
	});
});

var mobile_nav = {
  'message': function() {
    $('div.sidebar').addClass('hidden-xs hidden-sm');
    $('div.message').removeClass('hidden-xs hidden-sm');
  },
  'sidebar': function() {
    $('div.message').addClass('hidden-xs hidden-sm');
    $('div.sidebar').removeClass('hidden-xs hidden-sm');
  }
}

function switch_room(target_room){

  // Mobile navigation
  mobile_nav.message();

  var room_id = Number(target_room.replace('room-',''));
  var room_name = _.filter(global_room_list, function(obj){ return (obj.id === room_id) })[0].name;

  $('span#room_title').text(room_name);

  global_room_list.forEach( function(room){

    var room_num = 'room-' + room.id;
    if (room_num === target_room) {
      $('div.messagecontent').filter('#' + room_num).show();
      $('div#room-list a').filter('#' + room_num).attr('class', 'list-group-item room-link active');
    } else {
      $('div.messagecontent').filter('#' + room_num).hide();
      $('div#room-list a').filter('#' + room_num).attr('class', 'list-group-item room-link');
    }

  });

  // reset the badge count for the target room
  $('div#room-list a').filter( function(){ return $(this).attr('id') === target_room } ).children().filter('.badge').text('');

}

function get_message_data(room_id) {

    var message_endpoint = 'http://' + server_host + '/api/messages/?format=json';
    $.getJSON(message_endpoint, function(data){
      data.forEach(function(msg){
        message_room = Number(msg.room.split('/api/rooms/')[1].slice(0,-1));
        var message_text = msg.text.splice(msg.text.indexOf(':'),0,'</b>');
        message_text = message_text.splice(0,0,'<b>');
        if (message_room === room_id) { add_message(message_text, room_id) };
      });
    });

}

function populate_room_list() {

  $.getJSON('http://' + server_host + '/api/rooms/?format=json', function(data) { 
    // global_room_list = data;
    data.forEach(function(room) {
      add_new_room(room);
      get_message_data(room.id);
    });

    switch_room('room-' + global_room_list[0].id);

  });
}

function add_new_room(room) {
      var room_link = $('<a />', {
        'href': '#',
        'id': 'room-' + room.id,
        'class': 'list-group-item room-link'
      })
      .append( $('<span />', {
        'class': 'glyphicon glyphicon-comment padded-icon',
        'ariad-hidden': true
      }))
      .append(room.name)
      .append( $('<span />',{
        'class': 'badge'
      }));

      $('div#room-list').append(room_link);

      // add room to message list
      $('div#message_list').append( $('<div />', {
        'class': 'messagecontent',
        'id': 'room-' + room.id,
        'text': '',
      }));

     global_room_list.push(room);
     add_socket(room);
     $('div#room-' + room.id).hide();
}

function populate_user_list() {
  $.getJSON('http://' + server_host + '/api/users/?format=json', function(all_users) { 

    $.getJSON('http://' + server_host + ':3000/users', function(connected_users){

      // make sure the current user is included in the list
      connected_users.push(user);
      online_users = _.unique(connected_users);

      global_user_list = all_users;
      all_users.forEach(function(user) {
        var user_link = $('<li />', {
          'class': _.contains(online_users, user.username) ? 'user' : 'user disabled',
          'html': 
          $('<a />', {
            'href': '#'
          })
          .append( $('<span />', {
            'class': 'glyphicon glyphicon-user padded-icon'
            })).append(user.username)
        })

        $('ul.user_list').append(user_link);

      });
    });
  });
}

//upload file
function filechoose(){
  $("#inputmodal").modal('show');
}

$(document).on('change', '.btn-file :file', function() {
  var input = $(this),
      numFiles = input.get(0).files ? input.get(0).files.length : 1,
      label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
  input.trigger('fileselect', [numFiles, label]);
});

$(document).ready( function() {
    $('.btn-file :file').on('fileselect', function(event, numFiles, label) {
        
        var input = $(this).parents('.input-group').find(':text'),
            log = numFiles > 1 ? numFiles + ' files selected' : label;
        
        if( input.length ) {
            input.val(log);
        } else {
            if( log ) alert(log);
        }        
    });
});

// MAIN
$(document).ready(function(){

  populate_room_list();
  populate_user_list();

  $('div#room-list').on('click', 'a', function(){ 
    if ($(this).attr('id') != 'create-room' ) {
      switch_room( $(this).attr('id') );
    }
  });

  mobile_nav.sidebar();

  $('form#file_upload').submit(function(event){
    $.ajax({
      url: 'http://' + server_host + ':3000/upload',
      type: 'POST',
      data: new FormData( this ), 
      processData: false,
      contentType: false,
      success: function(file_path){ 
        var download_url = 'http://' + server_host + '/' + file_path;
        var display_name = $('input#filename').val();
        $('input#text').val('<a href="' + download_url + '">' + display_name + '</a>' );
        display();
        $('#inputmodal').modal('hide');
      }
    });
    event.preventDefault();
  });

});

$(document).ready(function(){
 function get_search_results() {
     $("searchResults").val("");
     var queryString = $("#search_box").val();
     var message_endpoint = 'http://' + server_host + '/api/messagesearch/?search=' + queryString;
     $.getJSON(message_endpoint, function(data){
       data.forEach(function(msg){
         if (msg.text.indexOf('::') != -1) {
           Object.getOwnPropertyNames(emoji_image).forEach( function(emoji){ msg.text = msg.text.replace(emoji, emoji_image[emoji]); });
         }
         $("#searchResults").append('<b>User:</b> ' + msg.user.username + '<br>' +
                  '<b>Room:</b> ' + msg.room.name + '<br>' +
                  '<b>Time:</b> ' + new Date(msg.time) + '<br>' +
                  '<b>Message:</b> ' + msg.text.slice(msg.user.username.length + 2) + '<br>' +
                  '<br>');
       });
     });
     $("#searchModal").modal('show');
     $('#searchResults').text('');
     $("#search_box").val("");
 }

 $("#search_box").keyup(function (e) {
     if (e.which == 13) {
     get_search_results();
   }
   return false;
 });

 $("#search_button_box").click(function () {
   get_search_results();
 });
}); 
