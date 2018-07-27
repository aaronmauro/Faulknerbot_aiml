var $messages = $('.messages-content'),
    d, h, m,
    i = 0;

$(function () {
  $('[data-toggle="popover"]').popover()
});

$(window).load(function() {
  $messages.mCustomScrollbar();
  setTimeout(function() {
    //fakeMessage();
  }, 100);
});

function updateScrollbar() {
  $messages.mCustomScrollbar("update").mCustomScrollbar('scrollTo', 'bottom', {
    scrollInertia: 10,
    timeout: 0
  });
}

function setDate(){
  d = new Date()
  if (m != d.getMinutes()) {
    m = d.getMinutes();
    $('<div class="timestamp">' + d.getHours() + ':' + m + '</div>').appendTo($('.message:last'));
  }
}



function insertMessage() {
  msg = $('.message-input').val();
  if ($.trim(msg) == '') {
    return false;
  }
  $('<div class="message message-personal">' + msg + '</div>').appendTo($('.mCSB_container')).addClass('new');
  setDate();
  $('.message-input').val(null);
  	updateScrollbar();
	interact(msg);
  setTimeout(function() {
    //fakeMessage();
  }, 1000 + (Math.random() * 20) * 100);
}

$('.message-submit').click(function() {
  insertMessage();
});

$('.clickable').click(function(){
    	find(msg);
    });

$(window).on('keydown', function(e) {
  if (e.which == 13) {
    insertMessage();
    return false;
  }
})

function interact(message){
	// loading message
  $('<div class="message loading new"><figure class="avatar"><img src="/static/res/botim.png" /></figure><span></span></div>').appendTo($('.mCSB_container'));
	// make a POST request [ajax call]
	$.post('/message', {
		msg: message
	}).done(function(reply) {
		// Message Received
		// Remove loading meassage
    $('.message.loading').remove();
		// Add message to chatbox
    $('<div class="message new"><figure class="avatar"><img src="/static/res/botim.png" /></figure>' + reply['text'] + '</div>').appendTo($('.mCSB_container')).addClass('new');
    setDate();
    updateScrollbar();

		}).fail(function() {
				alert('error calling chat function');
				});
}


// search and messages

function find(message){
	// loading message
  $('').appendTo($('.mCSB_container'));
	// make a POST request [ajax call]
	$.post('/_searcher', {
		msg
		//reply['text']
	}).done(function(reply) {
		// Message Received
		// Remove loading meassage
    $('.message.loading').remove();
		// Add message to chatbox
    $('<div class="message new"><figure class="avatar"><img src="/static/res/archiveim.png" /></figure>' + reply['text'] + '</div>').appendTo($('.mCSB_container')).addClass('new');
    setDate();
    updateScrollbar();

		}).fail(function() {
				alert('error calling search function');
				});
}

