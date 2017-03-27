$(function() {
	var placeInterval;
	function refreshEmails() {
		$('#results ul').html('');

		var dateRange = $('#date-range').val();

		$.post('/emails', {date_range: dateRange}, function(res) {
			var randomWidth, randomHeight;
			$.each(JSON.parse(res), function(i, email) {
				randomWidth = ($('#results').width()- 128) * Math.random();
				randomHeight = (window.innerHeight - $('#navbar').height() - 200) * Math.random();
				$('#results ul').append('<li style="top:'+randomHeight+';left:'+randomWidth+';"> \
					<a href="/email/' + email.message_id + '" class="subject">' + email.subject + '</a> \
				</li>');
			});

			// // Need to add click handlers to these new kids
			// $('#results ul li').click(function() {
			// 	$('.text.open').removeClass('open');
			// 	$(this).find('.text').addClass('open');
			// });
		});
	}

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
