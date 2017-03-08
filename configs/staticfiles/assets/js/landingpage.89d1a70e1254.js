var screenHeight = $(window).height(); 
		var belowheader = $('#below-header').outerHeight(true);

		var divcontainer = $('#my_tours');
		// Assign that height to the .row
		divcontainer.css({
			'height': (screenHeight-belowheader-belowheader) + 'px',
		});