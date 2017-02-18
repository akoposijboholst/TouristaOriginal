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
    var obj ={};
    for(var i = 0 ; i < elements.length ; i++){
        var item = elements.item(i);
        obj[item.name] = item.value;
    }

    alert(JSON.stringify(obj));

    // document.getElementById("demo").innerHTML = JSON.stringify(obj);
}