$(function() {
	var placeInterval;
	var width = ($('#results').width()- 128) * Math.random(),
		height = (window.innerHeight - 200) * Math.random();

	function refreshEmails() {
		$.get('/random-email', function(res) {
			res = JSON.parse(res);
			var maxDate = res["max_date"]["$date"],
				minDate = res["min_date"]["$date"],
				emailDate = res["email"]["date"]["$date"],
				email = res["email"]
			var normalizedTime = (emailDate - minDate) / (maxDate - minDate),
				normalizedMonth = new Date(emailDate).getMonth()/12;
			
			var randomWidth = $('#results').width() * (normalizedMonth - 1/12) + (Math.random() * 50),
				randomHeight = (window.innerHeight - 100) - ((window.innerHeight - 100) * normalizedTime);
			
			$('#results ul').append('<li style="top:'+randomHeight+';left:'+randomWidth+';"> \
				<a target="_blank" href="/email/' + email.message_id + '" class="subject">' + email.subject.replace("[Carpediem]", "") + '</a> \
				<p>' + new Date(emailDate).getFullYear() + '</p>\
			</li>');
		});
	}
	setInterval(refreshEmails, 1000);

	$('#date-range').daterangepicker({
		autoUpdateInput: false,
		locale: { cancelLabel: 'Clear' }
	});

	$('#date-range').on('apply.daterangepicker', function(ev, picker) {
		$(this).val(picker.startDate.format('MM/DD/YYYY') + ' - ' + picker.endDate.format('MM/DD/YYYY'));
		refreshEmails();
	});

	$('#date-range').on('cancel.daterangepicker', function(ev, picker) {
		$(this).val('');
	});
});
