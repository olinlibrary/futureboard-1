function getType(msg) {
  if (msg.data.indexOf('http') > -1) {
    return (msg.data.indexOf('youtu') > -1) ? 'video' : 'image';
  } else {
    return 'text';
  }
}

function placeTile(msg) {
  var type = getType(msg);
  var offsetX = (type !== 'text') ? 500 : 128;
  var offsetY = (type !== 'text') ? 400 : 200;
  randomWidth = ($('#results').width()- offsetX) * Math.random();
  randomHeight = (window.innerHeight - $('#navbar').height() - offsetY) * Math.random();

  switch (type) {
    case 'text':
      $('#results ul').append('<li style="top:'+randomHeight+';left:'+randomWidth+';"> \
        <p>' + msg.data +'</p>\
      </li>');
      break;
    case 'image':
      $('#results ul').append('<li style="top:'+randomHeight+';left:'+randomWidth+';"> \
        <img style="max-width: 500px;" src="'+ msg.data +'" />\
      </li>');
      break;
    case 'video':
      var url = msg.data.split('watch?v=')[1];
      $('#results ul').append('<li style="top:'+randomHeight+';left:'+randomWidth+';"> \
        <iframe width="560" height="315" src="https://www.youtube.com/embed/'+ url +'?rel=0&amp;autoplay=1&amp;controls=0&amp;showinfo=0" frameborder="0" allowfullscreen></iframe>\
      </li>');
      break;
  }
}

$(document).ready(function(){
  var protocol = (window.location.href.indexOf('https') > -1) ? 'https://' : 'http://';
  var socket = io.connect(protocol + document.domain + ':' + location.port + '/text');

  var randomWidth, randomHeight
  socket.on('response', placeTile);
});