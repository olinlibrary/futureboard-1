$(function() {
	function refreshEmails() {
		$('#results ul').html('');

		var dateRange = $('#date-range').val();
		var activeFilters = [];
		$('.options li.active').each(function() { activeFilters.push($(this).text().toLowerCase()); });

		$.post('/emails', {date_range: dateRange, topics: activeFilters.join(",")}, function(res) {
			$.each(JSON.parse(res), function(i, email) {
				$('#results ul').append('<li> \
					<div class="subject">' + email.subject + '</div> \
					<div class="text">' + email.text.trim().split('\n').join('<br>') + '</div> \
				</li>');
			});

			// Need to add click handlers to these new kids
			$('#results ul li').click(function() {
				$('.text.open').removeClass('open');
				$(this).find('.text').addClass('open');
			});
		});
	}

	$('ul.options li').click(function() {
		$(this).toggleClass('active');
		refreshEmails();
	});

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
