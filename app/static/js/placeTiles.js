function getType(msg) {
  var urlRegex = /(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9]\.[^\s]{2,})/;
  if (msg.data.match(urlRegex)) {
    if (msg.data.match(/(.jpg|.jpeg|.png|.gif|.tif)/)) {
      return 'image'
    } else {
      return (msg.data.match(/(youtu|vimeo)/)) ? 'video' : 'website';
    }
  } else {
    return 'text';
  }
}

function getRandomPosition(type) {
  var offsetX = (type !== 'text') ? 500 : 128,
    offsetY = (type !== 'text') ? 400 : 200;

  var randomWidth = ($('#results').width() - offsetX) * Math.random(),
    randomHeight = (window.innerHeight - $('#navbar').height() - offsetY) * Math.random();

  if (randomWidth < offLimits[0].width && randomHeight < offLimits[0].height) {
    randomHeight += offLimits[0].height;
  }
  
  // Code to come later for avoiding notification boxes

  return {
    top: randomHeight,
    left: randomWidth
  }
}

function placeTile(msg) {
  var type = getType(msg);
  var randomPos = getRandomPosition(type);
  var $li = $('<li id="'+ msg.date.$date.toString() +'" class="'+type+'" style="top:'+randomPos.top+';left:'+randomPos.left+';"></li>')

  switch (type) {
    case 'text':
      $li.html('<p>' + msg.data + '</p>');
      break;
    case 'image':
      $li.html('<img src="'+ msg.data +'" />');
      break;
    case 'video':
      if (msg.data.match(/vimeo/)) {
        var url = msg.data.split('.com/')[1];
        if (!url) return;
        $li.html('<iframe crossorigin="anonymous" src="https://player.vimeo.com/video/'+ url.split('?')[0] +'" width="640" height="360" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>');
      } else {
        var url = (msg.data.match(/\.be/)) ? msg.data.split('.be/')[1].split('?')[0] : msg.data.split('watch?v=')[1].split('&')[0];
        $li.html('<iframe width="560" height="315" src="https://www.youtube.com/embed/'+ url +'?rel=0&amp;controls=0&amp;showinfo=1" frameborder="0" allowfullscreen></iframe>');
      }
      break;
    case 'website':
      // cross origin makes iframes tricky
      // $li.html('<iframe width="600" height="400" src="'+ msg.data +'"></iframe>');
      break;
  }

  $('#results ul').append($li);
  $('#' + msg.date.$date.toString()).draggable();
}

function changeDate(day) {
  var ref = new Date();
  ref.setDate(ref.getDate() + parseInt(day));
  $('#results ul li').each(function(i, post) {
    if (ref.getTime() < parseInt(post.id)) {
      $(post).fadeOut();
    } else {
      $(post).fadeIn();
    }
  });
}

function placeEvent(event) {
  $('#events').append('<li id="" class="event">'+ event.data +'</li>')
}

$(document).ready(function(){
  var protocol = (window.location.href.indexOf('https') > -1) ? 'https://' : 'http://';
  var socket = io.connect(protocol + document.domain + ':' + location.port + '/text');

  // So that newly placed cards don't go above/underneath UI elements
  window.offLimits = [{  // First is the number in the top left that we 
    'x': 0,           // know will be there.
    'y': 0,
    'width': $('#number').width() + 30,  // Margin is 20, plus 10 padding
    'height': $('#number').height() + 40 // Margin is 30, plus 10 padding
  }]
  socket.on('response', placeTile);

  $('#number').click(function() {
    $('#date').val(0);
    $('#results ul li').hide();
  });

  var start = new Date(),
    end = new Date();
  end.setDate(end.getDate() + 2);
  start.setDate(end.getDate() - 1);
  $.get('/events?start=' + start.toString() + '&end=' + end.toString(), function(eventList) {
    eventList = JSON.parse(eventList);
    for (var i=0; i<eventList.length; i++) placeEvent(eventList[i]);
  });

  end.setDate(end.getDate() - 1);
  start.setDate(end.getDate() - 6);
  $.get('/texts?start=' + start.toString() + '&end=' + end.toString(), function(texts) {
    texts = JSON.parse(texts);
    for (var i=0; i<texts.length; i++) placeTile(texts[i]);
  });
});