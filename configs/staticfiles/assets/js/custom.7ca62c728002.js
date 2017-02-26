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

function logIn(e) {
	var email = document.getElementById("email").value;
	var password = document.getElementById("password").value;
	var json = '{ "email:" ' + email + ', "password":' + password + "}";
	$.ajax({
      type:'POST',
      url:'api/authenticate',
      cache:false,
      data:JSON.parse(json),
      async:asynchronous,
      dataType:json, //if you want json
      success: function(data) {
        // <put your custom validation here using the response from data structure >
      },
      error: function(request, status, error) {
        // <put your custom code here to handle the call failure>
      }
   });
}