var status = $('#status');
var maccy = "0000";

$(document).ready(function(){
	$.get('/api/devices', function(data, status){
		
	});
	
	$("#submitForm").click(function() {
		document.getElementById("progBarContainer").style.visibility = "visible";
		document.getElementById("progBar").style.visibility = "visible";

		var fData = $("#config_details").serialize();
		 $.ajax({
			url: '/api/submitform',
			type: 'POST',
			data: JSON.stringify(fData)
		});
	});

	function objectifyForm(formArray) {//serialize data function

		var returnArray = {};
		for (var i = 0; i < formArray.length; i++){
			returnArray[formArray[i]['name']] = formArray[i]['value'];
		}
		return returnArray;
	}

	function refresh(){
		$.get('/api/statusUpdate', function(data, status){
			console.log(`${data}`)
			document.getElementById("progBar").style.width = parseInt(`${data}`) + '%';
			document.getElementById("progBar").innerHTML = parseInt(`${data}`)*1 + '%';
			if(parseInt(`${data}`) < 100){	
				setTimeout(refresh, 5000);
			}				
		});
			
	}
});
	
function selectDevice() {
	var devSelBox = document.getElementById("devSel");
	if(devSelBox.selectedIndex){
		
		var dbgBox = document.getElementById("dbgg");
		var macStartBox = document.getElementById("macStart");
		var macEndBox = document.getElementById("macEnd");
		
		document.getElementById("configOptions").style.visibility = "visible";
		document.getElementById("config_details").style.visibility = "visible";
		
		switch(devSelBox.selectedIndex){
		case 1:
			maccy = "5003";
		break;
		
		case 2:
			maccy = "50DC";
		break;
		
		case 3:
			maccy = "5001";
		break;
		}
		
		macStartBox.value = maccy;
		macEndBox.value = maccy;
	}
}

function closeTab(){	
	$.ajax({
		type: "POST",
		url: '/api/tabClosed',
	});
	return;
}