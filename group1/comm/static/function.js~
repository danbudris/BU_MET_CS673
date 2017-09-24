

  var server_host = window.location.hostname;

  var socket = io('http://' + server_host + ':3000');

  var username = random_user();

       function _b()
       { 
      if(event.keyCode ==13)
      display();
      } 
       
  // Get the messages from the API and add to the page
  $.getJSON('http://' + server_host + '/api/messages/?format=json', function(json) {

    json.results.forEach(function(msg){
      add_message(msg.text);
    });

  });

  // When you receive a message, add it to the page
  socket.on('msg', function(msg){
    add_message(msg);
  });

  function add_message(msg) {
    $('div#messagecontent').append(msg + '<br>');
  }

  // Called when button is clicked
  function display() {
    var message = username + " : " + document.getElementById("text").value;
    socket.emit('msg', message);
  }
//input enter to send message too
  function _b(){
   if (event.KeyCode==13)
    display();
}
  // Generate random user
  function random_user() {
    var random_index = Math.floor( Math.random() * 100 ) + 1;
    return "User " + random_index;
  }

