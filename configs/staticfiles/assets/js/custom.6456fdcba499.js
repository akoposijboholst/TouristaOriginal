(function(){
	$("#login").click(function (event){
		login();
	});
});


function onClick(e){
	var number = document.getElementById('numberticker');
	var p = document.getElementById('number-me');
	var cur = number.value;
	if(e == 1){
		if (cur > 1)
			number.value = --cur;
		// $('#number').text(++number);
	}else{
		number.value = ++cur;
	}
	p.innerHTML = number.value;
}

function onClickAccommodation(e){
	var number = document.getElementById('numbertickeracc');
	var p = document.getElementById('number-accommodation');
	var cur = number.value;
	if(e == 1){
		if (cur > 1)
			number.value = --cur;
		// $('#number').text(++number);
	}else{
		number.value = ++cur;
	}
	p.innerHTML = number.value;
}

function addNewRow(e){
	var table = document.getElementById("myTable");
	var newRow = '<tr><td><input type="text" name="spotname2"></td><td><input type="text" name="activity1"></td><td><input type="text" name="time3"></td></tr>';
	table.append(newRow);
}

function logIn() {
    var elements = document.getElementById("login").elements;
    var inputs = $('#login').serialize;
    var formObj = {};
    $.each(inputs, function (i, input) {
        formObj[input.name] = input.value;
    });

    alert(JSON.stringify(formObj));

    // document.getElementById("demo").innerHTML = JSON.stringify(obj);
}