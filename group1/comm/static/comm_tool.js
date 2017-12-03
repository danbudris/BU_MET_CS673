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

function showCommDialog(actionUrl){
  $.ajax({
    type: "GET",
        url: actionUrl,
        success: function(result) {
          $("#dialogCommModal").html(result);
            $("#dialogCommModal").modal({
                backdrop: false,
                show: true
            });
        },
        async:true
    });
}

// close Story Dialog and erase the content
function closeDialog(){
  $("#dialogCommModal").modal('hide');
    $("#dialogCommModal").html('');
}

function scroll_messages_into_view() {
    if ($('span.msg p').length > 0) {
        var last_message_idx = $('span.msg p').length - 1;
        var last_msg_id = $('span.msg p')[last_message_idx].id;
        document.getElementById(last_msg_id).scrollIntoView();
    }
}

/*
function startVideoChat() {
  var teamName = window.document.documentElement.querySelector('#room_title').textContent;
  if (teamName != "" || teamName != null) {
    var URL = 'https://appr.tc/r/' + teamName.replace(' ','');
    window.open(URL, '', 'width=1000');

    //show the video area by removing the 'hide' class
    $('#videoArea').removeClass('hide');

    //set the iframe in the video area to the url of the video chat
    $('#videoFrame').attr('src', URL);
  } else {
    alert("Please create a team to be able to video chat")
  }
}
*/


//Set the sentinel for turning on/off the chat window
let chatcounter = 0; 

//Function for starting and stopping the video chat
function startVideoChat() {
  if (chatcounter == 0) {
    //increment the counter to 'on'
    chatcounter = 1;
    //set the URL to the video chat HTML api, and show the div containing it
    let URL = '/communication/videochat'
    $('#videoArea').removeClass('hide');
    $('#videoFrame').attr('src', URL);
    //shrink the scroll area that houses the messages to allow the shown div to fit
    $('.scroll-area').css("max-width", "50%");
    console.log("on");
  }
  else if (chatcounter == 1) {
    chatcounter = 0;
    let URL = ''
    $('#videoArea').addClass('hide');
    $('#videoFrame').attr('src', URL);
    $('.scroll-area').css("max-width", "100%");
    console.log("off");
  }
}

function createteam(){
  //Show modal to create team
  $("#deleteButton").remove();
  $("#myModal").modal('show');
  $("#saveTeam").attr('onclick', 'createTeamFunc()');
  $("#modalName").text("Create New Team");
  $("#teamname").val('');
}

var curroom;

function editteam(){
  //Get the current room that the user is in
  curroom = getCurrentRoom();
  //Check if current room was created by the user who is attempting to edit it
  if (curroom.creator == 'http://' + server_host + ':' + server_port + '/api/users/' + user_id + '/' || curroom.creator == 'http://localhost:8000/api/users/' + user_id + '/') {
    //Show modal to edit or delete team
    $("#deleteButton").remove();
    $("#myModal").modal('show');
    $("#saveTeam").attr('onclick', 'editTeamFunc()');
    $("#modalName").text("Edit Team");
    $("#teamname").val(curroom.name);
    $("<button type='button' class='btn btn-default' id='deleteButton' onclick='deleteTeamFunc()'>Delete Team</button>").insertBefore("#cancelButton");
  } else {
    alert("You do not have permission to edit this room!");
  }
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
 var global_indv_room=[];


var server_host = window.location.hostname;
var server_port = window.location.port;
var base_url = 'http://' + server_host + ':3000/';
var global = io('http://' + server_host + ':3000');

userVisit={};
userVisitedDate=[];
$.getJSON('http://' + server_host + ':' + server_port + '/api/userVisit/',function(data){
    userVisitedDate=data;
    data.forEach(function(data){
       userVisit[data.id]=data.user;

    });
});

global.emit('user', {
  'username': user,
   'userId':user_id,
    'visitStatus':userVisit,
  'action': 'connect',
});

global.on('room', function(room) {
  add_new_room(room);
  switch_room('room-' + room.id);
});

global.on('updateroom', function(room) {
  //Update the heading and sidebar to reflect changes
  $('span#room_title').text(room.name);
  var room_link_html = "<span class='glyphicon glyphicon-comment padded-icon' ariad-hidden='true'></span>" + room.name + "<span class='badge'></span>";
  $('a#room-' + room.id).html(room_link_html);

  //Update the global room list with new name
  var i;
  for (i = 0; i < global_room_list.length; i++) {
    if (global_room_list[i].id == room.id) {
      global_room_list[i] = room;
      break;
    }
  }
  $("#myModal").modal('hide');
});

global.on('deleteroom', function(room) {
  //Remove the team from the sidebar
  $("#room-" + room.id).remove();
  for (i = 0; i < global_room_list.length; i++) {
    if (global_room_list[i].id == room.id) {
      global_room_list.splice(i, 1);
      break;
    }
  }
  $("#myModal").modal('hide');
  switch_room('room-' + global_room_list[0].id);
});

global.on('editmsg', function(msg) {
  //Make username bold
  var message_text = msg.text.splice(msg.text.indexOf(':'),0,'</b>');
  message_text = message_text.splice(0,0,'<b>');
  //Change message text
  $("p#message-" + msg.id).html(message_text);
});

global.on('deletemsg', function(msgid){
  //Remove span element that contains message
  $("p#message-" + msgid).parent().remove();
});

function createTeamFunc() {

    var new_team_name = $('input#teamname').val();
    if (!testNameValidation(new_team_name)) {
      alert("Please enter a valid team name");
    } else if (!isTeamNameExist(new_team_name)) {
      alert("A team with that name already exist.");
    } else {
      var room_data = {
        name: new_team_name,
        creator_id: user_id,
        description: 'test',
        public: true
      };

      global.emit('room', room_data);

      $("#myModal").modal('hide');
    }
}

function testNameValidation(text) {
  if(text.trim() == null || text.trim() == "" || /^[a-zA-Z0-9- ]*$/.test(text) == false) {
    return false;
  } else {
    return true;
  }
}

function isTeamNameExist(new_team_name) {
  var isNameValid = true;
  for (i = 0; i < global_room_list.length; i++) {
    if (global_room_list[i].name == new_team_name) {
      isNameValid = false;
    }
  }
  return isNameValid;
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
$.getJSON('http://' + server_host + ':' + server_port + '/api/rooms/',function(data){
  data.forEach(function(room){
    //add_socket(room);
  });
});

function add_socket(room) {
    var socket = io(base_url + room.id);
    socket.on('msg', function(msg) {
      if (msg.already_sent === true) {
          return;
      }
      if (room.id != visible_namespace()) {
        increment_badge(room.id);
      }
      var message_user = Number(msg.user.split('/api/users/')[1].slice(0,-1));
      var message_text = msg.text.splice(msg.text.indexOf(':'),0,'</b>');
      message_text = message_text.splice(0,0,'<b>');
      add_message(message_text, msg.id, message_user, room.id, msg.time);
      msg.already_sent = true;

      if ($('span.msg p').length > 0) {
          var last_message_idx = $('span.msg p').length - 1;
          var last_msg_id = $('span.msg p')[last_message_idx].id;
          document.getElementById(last_msg_id).scrollIntoView();
      }
    });

    sockets[room.id] = socket;
}


function increment_badge(room_id){
  var badge = $('div#room-list a').filter( function(){ return $(this).attr('id') === 'room-' + room_id } ).children().filter('.badge');
  var count = Number(badge.text());
  badge.text(count += 1);
}
var sent_day_check=null;
function add_message(msg, msgid, msguser, target, date) {

  //Check if user is the person who sent message. Show different options depending on result.
  //The p element contains the actual message, and each of them have the id "message-" followed by the message id
    var sent_day=messageSentDay(date);
    if(sent_day!=null){
        //alert(sent_day);
        if(sent_day_check!=sent_day){
            sent_day_check=sent_day;
            sent_day='<br><b><i style="color: #33A8FF">'+sent_day_check+'</i></b><br><br>';
            //sent_day='<p style="color: #33A8FF"><b><i>'+sent_day_check+'</i></b></p><br>';
        }
        else{
            sent_day='';
        }
    }

    var sent_time=date.split('-')[2].slice(3, 8);
    var send_name=msg.split(':')[0];
    var check_result=checkForAudioRecord(msg);
    if (check_result.slice(0, 10)=='blob:http:'){
        if(msguser == user_id){
            $('div#room-' + target).append('<span class="msg"><p id="message-' + msgid + '">' + '<div id="player">'+sent_day+'<small>'+sent_time+'</small>&nbsp;<b>'+send_name+':</b><audio controls><source src="'+check_result+'" type="audio/ogg"></audio></div>' + '</p><span class="msgoptions"><img src="/static/emoji/happy.jpg" style="width:15px;height:15px;margin-right:5px;">...</span><ul class="msgmenu"><li onclick="deleteMessage(' + msgid + ')" class="red">delete</li></ul></span>');
        }
        else {
            $('div#room-' + target).append('<span class="msg"><p id="message-' + msgid + '">'+sent_day+'<small>'+sent_time+'</small>&nbsp;<b>'+send_name+':</b>' + '<audio controls><source src="'+check_result+'" type="audio/ogg"></audio>' + '</p><span class="msgoptions"><img src="/static/emoji/happy.jpg" style="width:15px;height:15px;margin-right:5px;">...</span></span>');
        }
    }
    else {
        if (msguser == user_id) {
            $('div#room-' + target).append('<span class="msg"><p id="message-' + msgid + '">'+sent_day+'<small>'+sent_time+'</small>&nbsp;' + msg + '</p><span class="msgoptions"><img src="/static/emoji/happy.jpg" style="width:15px;height:15px;margin-right:5px;">...</span><ul class="msgmenu"><li onclick="showEditMessage(' + msgid + ')">edit</li><li onclick="deleteMessage(' + msgid + ')" class="red">delete</li></ul></span>');
        } else {
            $('div#room-' + target).append('<span class="msg"><p id="message-' + msgid + '">'+sent_day+'<small>'+sent_time+'</small>&nbsp;' + msg + '</p><span class="msgoptions"><img src="/static/emoji/happy.jpg" style="width:15px;height:15px;margin-right:5px;">...</span></span>');
        }
    }
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
function checkForAudioRecord(msg){
    var check=msg.split(':')[0];
    return msg.slice(check.length+1, msg.length);

}
function messageSentDay(data){
    var sent_weekday=null;
    var sent_day=null;
    var sent_month=null;
    var weekday = new Array(7);
    weekday[0] =  "Sunday";
    weekday[1] = "Monday";
    weekday[2] = "Tuesday";
    weekday[3] = "Wednesday";
    weekday[4] = "Thursday";
    weekday[5] = "Friday";
    weekday[6] = "Saturday";
    var month = new Array();
    month[1] = "January";
    month[2] = "February";
    month[3] = "March";
    month[4] = "April";
    month[5] = "May";
    month[6] = "June";
    month[7] = "July";
    month[8] = "August";
    month[9] = "September";
    month[10] = "October";
    month[11] = "November";
    month[12] = "December";
    var time=data.split("-");
    var year=time[0];
    var months=time[1];
    var day=time[2].slice(0, 2);
    var hours=time[2].slice(3, 5);
    var minutes=time[2].split(":")[1];
    console.log(year+":"+months+":"+day+":"+hours+":"+minutes);
    var d=new Date(year, months, day, hours, minutes);
    var currentTime=new Date();
    if(d.getYear()==currentTime.getYear()){
        if (d.getMonth()==(currentTime.getMonth()+1)){
            var sent_day_range=currentTime.getDate()-d.getDate();
            if (sent_day_range<7){

                if (sent_day_range==0){
                    sent_weekday='Today';
                }
                else if (sent_day_range==1){
                    sent_weekday='Yesterday';
                }
                else {
                    sent_weekday=weekday[d.getDay()];
                }
            }
            else {
                sent_day=month[d.getMonth()]+' '+d.getDate();
            }
        }
        else {
            sent_month=month[d.getMonth()]+' '+d.getDate();
        }

    }
    if(sent_weekday!=null){
        return sent_weekday;
    }
    else if (sent_day!=null){
        return sent_day;
    }
    else if(sent_month!=null){
        return sent_month;
    }
    else {
        return '';
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
  if($("#text").val().length == 0){
    return;
  }
  var message = {
    'username': user,
    'value': $('input#text').val(),
    'user_id': user_id,
    'already_sent': false
  };

  if(getCurrentRoom()){
       sockets[visible_namespace()].emit('msg', message);
       $('input#text').val('');
       $("#charLimitMessage").css("display", "none");
  }
  else {
      global.emit('indv_msg', message);
      $('input#text').val('');
      $("#charLimitMessage").css("display", "none");
  }


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
};

function switch_room(target_room){

  /* shut off the video when a room is changed
     This should, in the end, open a NEW room, with a new chat, rather than cancelling the existing chat
     This could be done by having 'start video chat' create a new div which is only 'unhidden' when the given room is in use; otherwise, 
     it's hidden; each existing room with a video chat would have one, and on switch the class 'hidden' would be toggled onto that room; on open, it would be toggled off 
  */
  chatcounter = 1;
  startVideoChat();

  // Mobile navigation
    //hide indv romm
    sent_day_check=null;
    if(visible_namespace()){
        var hide_indv_room = 'room-'+visible_namespace();
        $('div.messagecontent').filter('#' + hide_indv_room).hide();
    }

  mobile_nav.message();


  var room_id = Number(target_room.replace('room-',''));
  var room_name = _.filter(global_room_list, function(obj){ return (obj.id === room_id) })[0].name;

  $('span#room_title').text(room_name);

  global_room_list.forEach( function(room){

    var room_num = 'room-' + room.id;
    console.log('room_num '+room_num);
    console.log('target_room '+target_room);
    if (room_num === target_room) {
        $('div#room-list a').filter('#' + room_num).attr('class', 'list-group-item room-link active');
      $('div.messagecontent').filter('#' + room_num).show();

    } else {
      $('div.messagecontent').filter('#' + room_num).hide();
      $('div#room-list a').filter('#' + room_num).attr('class', 'list-group-item room-link');
    }

  });

  // reset the badge count for the target room
  $('div#room-list a').filter( function(){ return $(this).attr('id') === target_room } ).children().filter('.badge').text('');

  document.getElementById("bottom").scrollIntoView();
 $('html, body').animate({ scrollTop: $(document).height() }, 1200);
}

// get message for specific room
// @param - room_id
function get_message_data(room_id) {


    var message_endpoint = 'http://' + server_host + ':' + server_port + '/api/messages/?room=' + room_id
    + '&' + 'format=json';
    $.getJSON(message_endpoint, function(data){
      data.forEach(function(msg){
        message_room = Number(msg.room.split('/api/rooms/')[1].slice(0,-1));
        var message_user = Number(msg.user.split('/api/users/')[1].slice(0,-1));
        var message_text = msg.text.splice(msg.text.indexOf(':'),0,'</b>');
        message_text = message_text.splice(0,0,'<b>');
        add_message(message_text, msg.id, message_user, room_id, msg.time) ;
      });
    });
}

// audio recording starts
function startRecording() {

navigator.getUserMedia = navigator.getUserMedia ||
                         navigator.webkitGetUserMedia ||
                         navigator.mozGetUserMedia;
//var record = document.querySelector('#record');
var record = document.getElementById("record");
var audioURL;

if (navigator.getUserMedia) {
   console.log('getUserMedia supported.');
   navigator.getUserMedia (
      // constraints - only audio needed for this app
      {
         audio: true
      },

      // Success callback
      function(stream) {
        var mediaRecorder = new MediaRecorder(stream);
        record.onclick = function() {
          mediaRecorder.start();
          console.log(mediaRecorder.state);
          console.log("recorder started");
          record.style.background = "red";
          record.style.color = "black";
          record.id = "stop";
          setTimeout(function(){
            console.log("recorder stopped");
            mediaRecorder.stop();
            console.log(mediaRecorder.state);
            console.log("recorder stopped");
            record.style.background = "";
            record.style.color = "";
          }, 5000);

        }

        var chunks = [];

          mediaRecorder.ondataavailable = function(e) {
          chunks.push(e.data);
        };
        mediaRecorder.onstop = function(e) {
            console.log("recorder stopped");


            var blob = new Blob(chunks, { 'type' : 'audio/ogg; codecs=opus' });
            console.log("blob = "+blob);
            chunks = [];
            audioURL = window.URL.createObjectURL(blob);
            var message = {
                'username': user,
                'value': audioURL,
                'user_id': user_id,
                'already_sent': false
              };
            global.emit('indv_msg', message);
            scroll_messages_into_view();
            console.log("audioUrl = "+audioURL)
          }
      },
      // Error callback
      function(err) {
         console.log('The following gUM error occured: ' + err);
      }
   );
    } else {
   console.log('getUserMedia not supported on your browser!');
    }
}


// load all the room names for the user
function populate_room_list() {

  $.getJSON('http://' + server_host + ':' + server_port + '/api/rooms/?format=json', function(data) {
    // global_room_list = data;
    data.forEach(function(room) {
      add_new_room(room);
    });

    switch_room('room-' + global_room_list[0].id);
    get_message_data(global_room_list[0].id); // load messages for the first room

  });
}

function add_new_room(room) {
      var room_link = $('<a />', {
        'href': '#',
        'id': 'room-' + room.id,
        'class': 'list-group-item room-link'
      })

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
     switch_indvroom("remove"); // removing individual room
     $('div#room-' + room.id).hide();
}

function populate_user_list() {
  $.getJSON('http://' + server_host + ':' + server_port + '/api/users/?format=json', function(all_users) {

    $.getJSON('http://' + server_host + ':3000/users', function(connected_users){

      // make sure the current user is included in the list
      //connected_users.push(user);
      online_users = _.unique(connected_users);


      global_user_list = all_users;
      all_users.forEach(function(user) {
          add_new_indvRoom(user.id);
        var user_link = $('<li />', {
          'class': _.contains(online_users, user.id) ? 'user' : 'user',
          'id':user.id,
          'html':
          $('<a />', {
            'href': '#',
              'class': 'list-user-item user-link'

          })
        .append(user.username).append($('<span />',{
        'class': 'badge'
        }))
        });

        $('ul.user_list').append(user_link);

      });
    });

  });
}
function add_new_indvRoom(userId){
    $.getJSON('http://localhost:8000/api/indvrooms/?format=json', function (data) {
        var indvroom_id=0;
        data.forEach(function (room) {
            var room_users = room.users.split("-");
            if ((room_users[0] == user_id && room_users[1] == userId) || (room_users[0] == userId && room_users[1] == user_id)) indvroom_id = room.id;
        });
        if (indvroom_id == 0) global.emit('indvroom', {'creator_id': user_id, 'second_user': userId});
        global.emit('indvjoin', {"indvroom": indvroom_id});
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

function switch_indvroom(id) {
    sent_day_check=null;
    var room_num = 'room-' + visible_namespace();
    //$('div#room-list a').filter('#' + room_num).attr('class', 'list-group-item room-link');
    global_user_list.forEach(function (data) {
        if(data.id==id){
             $('ul.user_list li').filter('#' + data.id).find('a').attr('class', 'list-user-item user-link active');
          }
          else{
              $('ul.user_list li').filter('#' + data.id).find('a').attr('class', 'list-user-item user-link');
          }
    });
    var badge=$('ul.user_list li').filter(function(){ return $(this).attr('id') == id }).find('a').children().filter('.badge').text('');
}


function vidoeSend() {
    global.emit('indv_videoChat', {'some_data':'some_info'});
}
global.on('indv_videoChat_accept', function (data) {
    window.location.href='/communication/videochat';
});


// MAIN
$(document).ready(function(){
    startRecording();
  populate_room_list();
  populate_user_list();


// switch and load messages on click on the room name
  $('div#room-list').on('click', 'a', function(){
    if ($(this).attr('id') != 'create-room' ) {
      
      var id = $(this).attr('id').split("-");
      console.log("id: " + id[1]);
      clearMessage();
      switch_room( $(this).attr('id') );
      get_message_data(id[1]); // load messages for the room
      switch_indvroom('rm');

    }
  });


  $('ul.user_list').on('click', 'li', function(){
      var id = $(this).attr('id');
      if(user_id!=id) {
          switch_indvroom(id);

          var curRoomId=getCurrentRoom();
          if(curRoomId){
               var room_num = 'room-'+curRoomId.id;
                $('div#room-list a').filter('#' + room_num).attr('class', 'list-group-item room-link');
                $('div.messagecontent').filter('#' + room_num).hide();
          }
          var label_name = $(this).find('a').text();
          var online=checkForOnline(id);
          //alert(online);
          $('span#room_title').text(label_name);
          $('span#room_title').append(online);


          //console.log(JSON.stringify(global_user_list));

          clearMessage();

          $.getJSON('http://localhost:8000/api/indvrooms/?format=json', function (data) {

              var indvroom_id = 0;
              data.forEach(function (room) {
                  global_indv_room.push(room.id);
                  var room_users = room.users.split("-");
                  if ((room_users[0] == user_id && room_users[1] == id) || (room_users[0] == id && room_users[1] == user_id)) indvroom_id = room.id;


              });

              if (indvroom_id == 0) global.emit('indvroom', {'creator_id': user_id, 'second_user': id});
              global.emit('indvroom_id', {"id": indvroom_id});
              var check_messagelist = $('div#room-' + indvroom_id)[0];
              if (!check_messagelist) {
                  $('div#message_list').append($('<div />', {
                      'class': 'messagecontent',
                      'id': 'room-' + indvroom_id,
                      'text': '',
                  }));
              }

              get_indvroom_messages(indvroom_id);
              get_indvroom_show(indvroom_id);
              document.getElementById("bottom").scrollIntoView();
              $('html, body').animate({ scrollTop: $(document).height() }, 1200);
              var room_num = 'room-' + indvroom_id;
              global.emit('indvjoin', {"indvroom": indvroom_id});
          });
      }
  });



function checkForOnline(id) {
    //alert(online_users);
     for(var i=0; i<online_users.length; i++){
         if(online_users[i]==id && online_users[i]!=user_id){
             return "<small><small><sub><i>online</i></sub></small></small>";
         }
     }
     //console.log(JSON.stringify(userVisitedDate));
     var visitedDay;
     var visitedHour;
     var visitedMonth;
     var visitedYear;
     userVisitedDate.forEach(function (data) {
        var userID=Number(data.user.split('/api/users/')[1].slice(0,-1));
        if (userID==id){
            var time=data.time.split("-");
            var year=time[0];
            var months=time[1];
            var day=time[2].slice(0, 2);
            var hours=time[2].slice(3, 5);
            var minutes=time[2].split(":")[1];
            console.log(year+":"+months+":"+day+":"+hours+":"+minutes);
            var d=new Date(year, months, day, hours, minutes);
            var currentTime=new Date();
            if(currentTime.getYear()==d.getYear()){
                //alert(d.getMonth());
                if(currentTime.getMonth()+1==d.getMonth()){
                    if(currentTime.getDate()!=d.getDate()){
                        visitedDay=currentTime.getDate()-d.getDate();
                    }
                    else {
                        visitedHour=currentTime.getHours()-d.getHours();
                    }
                }
                else {
                    visitedMonth=(currentTime.getMonth()+1)-d.getMonth();
                }

            }
            else {
                visitedYear=currentTime.getYear()-d.getYear();
            }



        }
     });
     if(visitedDay){
         return "<small><small><sub><i>was online "+ visitedDay +" day(s) ago</i></sub></small></small>";
     }
     else if(visitedHour){
         return "<small><small><sub><i>was online "+ visitedHour +" hour(s) ago</i></sub></small></small>";
     }
     else if(visitedMonth){
         return "<small><small><sub><i>was online "+ visitedMonth +" month(s) ago</i></sub></small></small>";
     }
     else if(visitedYear){
         return "<small><small><sub><i>was online "+ visitedYear +" year(s) ago</i></sub></small></small>";
     }

}

function get_indvroom_show(indvroom_id) {
    for(var i=0; i<global_indv_room.length; i++){
        if(indvroom_id==global_indv_room[i]){
            var room_show = 'room-' + indvroom_id;
            $('div.messagecontent').filter('#' + room_show).show();
        }
        else {
            //alert(global_indv_room[i]);
            var room_hide = 'room-' + global_indv_room[i];
            $('div.messagecontent').filter('#' + room_hide).hide();
        }
    }
}

  function get_indvroom_messages(indvroom){
      $.getJSON('http://localhost:8000/api/indvmessages/?format=json', function(data) {
            data.forEach(function (messages) {
                if(messages.indv_room==indvroom){
                    var message=checkMessageFortext(messages.text);
                    var message_user = Number(messages.send_user.split('/api/users/')[1].slice(0,-1));
                    add_message(message, messages.id, message_user, messages.indv_room, messages.time);

                }
            })
      });

  }
   global.on('indv_msg', function (data) {
           var message=checkMessageFortext(data.text);
           var message_user = Number(data.send_user.split('/api/users/')[1].slice(0,-1));
           add_message(message, data.id, message_user, data.indv_room, data.time);
           scroll_messages_into_view();
           //alert(message);
           increment_indvBadge(message_user);
       });
  function increment_indvBadge(message_user){
      if(user_id!=message_user){
          var badge=$('ul.user_list li').filter(function(){ return $(this).attr('id') == message_user }).find('a').children().filter('.badge');
            var count = Number(badge.text());
            badge.text(count += 1);
      }
  }

  function checkMessageFortext(message){
      var text=message.split(':');
      if (text[1]!=' blob' && text[2]!='http') {
          return '<b>'+text[0]+'</b>:'+text[1];
      }
      else{
        var head=message.substring(0, text[0].length);
        var tile=message.substring(text[0].length+2, message.length);
        return '<b>'+head+'</b>:'+tile;
      }

  }

  // clear all messages
  function clearMessage(){
    $(".messagecontent p").remove();
  }

  mobile_nav.sidebar();

  $('form#file_upload').submit(function(event){
    $.ajax({
      url: 'http://' + server_host + ':3000/upload',
      type: 'POST',
      data: new FormData( this ),
      processData: false,
      contentType: false,
      success: function(file_path){
        var download_url = 'http://' + server_host + ':' + server_port + '/' + file_path;
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
     var message_endpoint = 'http://' + server_host + ':' + server_port + '/api/messagesearch/?search=' + queryString;
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


function checklength() {
  if($("#text").val().length == 1000){
    $("#charLimitMessage").css("display", "block");
  }else{
     $("#charLimitMessage").css("display", "none");
  }
}


function getCurrentRoom() {
  //The current room has the 'active' class in its div element
  var result;
  global_room_list.forEach( function(room){
    var room_num = 'room-' + room.id;
    if ($('div#room-list a').filter('#' + room_num).hasClass('active')) {
      result = room;
    }
  });

  return result;
}

function editTeamFunc() {
  var edited_team_name = $('input#teamname').val();
  if (!testNameValidation(edited_team_name)) {
    alert("Please enter a valid team name");
  } else if (!isTeamNameExist(edited_team_name)) {
    alert("A team with that name already exist. ");
  } else {
    var room_data = {
      id: curroom.id,
      name: edited_team_name,
      creator: 'http://' + server_host + ':' + server_port + '/api/users/' + user_id + '/',
      description: curroom.description,
      public: curroom.public,
    };
    global.emit('updateroom', room_data);
  }
}

function deleteTeamFunc() {
  if (confirm('Are you sure you would like to delete this team?')) {
    global.emit('deleteroom', curroom);
  } else {
    return false;
  }
}

function insertUserRoom(userid, roomid) {
    var userroom_data = {
        user: userid,
        room: roomid
    };
    global.emit('userroom', userroom_data);
}

function showEditMessage(msgid) {
  var prevmsg = $("p#message-" + msgid).text(); //Remember previous message
  var usr = prevmsg.slice(0, prevmsg.indexOf(":")); //Extract username from message
  var msg = prevmsg.slice(prevmsg.indexOf(":") + 2); //Extract text from previous message
  //Replace html inside p element with an input
  $("p#message-" + msgid).html("<b>" + usr + "</b>: <input id='edit-" + msgid + "' type='text' value='" + msg + "' style='width: 80%;' required>");

  $("input#edit-" + msgid).focus();//Automatically focus that input

  $("input#edit-" + msgid).keypress(function(e) {
    if(e.which == 13) {
      //When user hit enter:
      var newtext = usr + ": " + $("input#edit-" + msgid).val(); //New message text
      if (newtext != prevmsg) {
        editMessage(msgid, newtext);//Function to emit event
      } else {
        $("p#message-" + msgid).html("<b>" + usr + "</b>: " + msg);//Nothing changed so revert back
      }
    }
  });

  $("input#edit-" + msgid).focusout(function() {
    //If user clicks out, remove input and revert back to original view
    $("p#message-" + msgid).html("<b>" + usr + "</b>: " + msg);
  });
}

function editMessage(msgid, msgtext) {
  var message_data = {
    id: msgid,
    text: msgtext
  };
  if(getCurrentRoom()) global.emit('editmsg', message_data);
  else global.emit('editIndvmsg', message_data);

}

function deleteMessage(msgid) {
  //Use message id to delete
  if (confirm('Are you sure you would like to delete this message?')) {
      if(getCurrentRoom()) global.emit('deletemsg', msgid);
      else global.emit('deleteIndvmsg', msgid);
  } else {
    return false;
  }
}

// EVENT LISTENERS

$("#startVideo").click( ()=> {
  console.log('Attempting to start video');
  startVideoChat();
})

// The Browser API key obtained from the Google API Console.
var developerKey = 'AIzaSyBW8Ea4hPD4Xlo9Uo9pCiRK3CaTj1iT8cw';

// The Client ID obtained from the Google API Console. Replace with your own Client ID.
var clientId = "216454920265-v6i1auidua6oahnd8c92mhl2d1li5cct.apps.googleusercontent.com"

// Scope to use to access user's drive files.
var scope = ['https://www.googleapis.com/auth/drive'];

var pickerApiLoaded = false;
var isDownloadFiles = false;
var isUploadFiles = false;
var oauthToken;

// Use the API Loader script to load google.picker and gapi.auth.
function onApiLoad() {
  gapi.load('auth', {'callback': onAuthApiLoad});
  gapi.load('picker', {'callback': onPickerApiLoad});
}

function initDownloadFiles() {
  isDownloadFiles = true;
  onApiLoad();
}

function initUploadFiles() {
  isUploadFiles = true;
  onApiLoad();
}

function onAuthApiLoad() {
  window.gapi.auth.authorize(
    {
      'client_id': clientId,
      'scope': scope,
      'immediate': false
    },
    handleAuthResult);
}

function onPickerApiLoad() {
  pickerApiLoaded = true;
  createPicker();
}

function handleAuthResult(authResult) {
  if (authResult && !authResult.error) {
    oauthToken = authResult.access_token;
    createPicker();
  }
}

// Create and render a Picker object.
function createPicker() {
  if (pickerApiLoaded && oauthToken) {
    if (isDownloadFiles) {
      var picker = new google.picker.PickerBuilder().
        addView(google.picker.ViewId.DOCS).
        setOAuthToken(oauthToken).
        setDeveloperKey(developerKey).
        setCallback(downloadFileCallback).
        build();
    } else if (isUploadFiles) {
      var picker = new google.picker.PickerBuilder().
        addView(new google.picker.DocsUploadView()).
        setOAuthToken(oauthToken).
        setDeveloperKey(developerKey).
        setCallback(uploadFileCallback).
        build();
    }
    picker.setVisible(true);
  }
}

function downloadFileCallback(data) {
  if (data[google.picker.Response.ACTION] == google.picker.Action.PICKED) {
    var fileId = data.docs[0].id;
    var xhr = new XMLHttpRequest();
    xhr.open('GET', "https://www.googleapis.com/drive/v3/files/" + fileId +
        "/export?mimeType=text%2Fplain&key=" + developerKey);
    xhr.setRequestHeader('Authorization', 'Bearer' + oauthToken);
    xhr.send();
    isDownloadFiles = false;
  }
}

function uploadFileCallback(data) {
  isUploadFiles = false;
}
