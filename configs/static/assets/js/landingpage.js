var value = document.getElementById("json_text").value;
var json = JSON.parse(value);
var agencyName = json["agencyName"]
var $a = $('#agency-name');
var children  = $a.children();
$a.text(agencyName);
$a.append(children);


var screenHeight = $(window).height(); 
		var belowheader = $('#below-header').outerHeight(true);

		var divcontainer = $('#my_tours');
		// Assign that height to the .row
		divcontainer.css({
			'height': (screenHeight-belowheader-belowheader) + 'px',
		});