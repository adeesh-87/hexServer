//var status = $('#status');
var maccy = "0000";
var panBase = "0000";
var sessionId = "";
var tempPanBase = "";

$(document).ready(function(){
	
	var deviceSelect = document.getElementById("devSel");
	var chSelect = document.getElementById("chan");
	var projSelect = document.getElementById("project_select");
	// should not use plurals like devices, should be device singular
	$.get('/device/', function(data, status){
		var cfInit = JSON.parse(data);
		//console.log(devices);
		var devices = cfInit["devicelist"].split(',');
		for (d in devices){
			//console.log(devices[d]);
			var option = document.createElement("option");
			option.value = devices[d];
			option.text = devices[d];
			deviceSelect.add(option);
		}
		
		var channels = cfInit["GlobalConfigOptions"]["channel_masks"].split(',');
		for (ch in channels){
			var option = document.createElement("option");
			option.value = channels[ch];
			option.text = channels[ch];
			chSelect.add(option);
		}
		
		var projects = cfInit["project_codes"]
		for (key in projects){
			var option = document.createElement("option");
			option.value = projects[key];
			option.text = key;
			projSelect.add(option);
		}
		
		panBase = cfInit["GlobalConfigOptions"]["extended_pan_base"];
		tempPanBase = panBase;
		//console.log(channels);
	});
	


	function objectifyForm(formArray) {//serialize data function

		var returnArray = {};
		for (var i = 0; i < formArray.length; i++){
			returnArray[formArray[i]['name']] = formArray[i]['value'];
		}
		return returnArray;
	}
	
	
function closeTab(){	
	$.ajax({
		type: "POST",
		url: '/api/tabClosed',
	});
	return;
}
});

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
	
function selectDevice() {
	
	panBase = tempPanBase;
	var devSelBox = document.getElementById("devSel");
	//var devDetails;
	var projSelect = document.getElementById("project_select");
	var fixedPan = document.getElementById("fixedPan");
	var getReq = '/device/'.concat(devSelBox.value);
	panBase = panBase.concat(projSelect.value.padStart(3,'0'));
	fixedPan.innerHTML = panBase;
	fixedPan.value = panBase;
	console.log(getReq);
	$.get(getReq, function(data, status){
		console.log(data);
		var devDetails = JSON.parse(data);
		//console.log(devDetails);
		var dbgBox = document.getElementById("dbgg");
		var macStartBox = document.getElementById("macStartBase");
		var macEndBox = document.getElementById("macEndBase");
		var devVersions = document.getElementById("versions");
		document.getElementById("configOptions").style.visibility = "visible";
		document.getElementById("config_details").style.visibility = "visible";
		maccy = devDetails["macbase"];
		var dVersions = devDetails["versions"].split(',');
		for (ver in dVersions){
			var option = document.createElement("option");
			option.value = dVersions[ver];
			option.text = dVersions[ver];
			devVersions.add(option);
		}
		macStartBox.innerHTML = maccy.concat(projSelect.value.padStart(3,'0'));
		macStartBox.value = maccy.concat(projSelect.value.padStart(3,'0'));
		macEndBox.innerHTML = maccy.concat(projSelect.value.padStart(3,'0'));
		macEndBox.value = maccy.concat(projSelect.value.padStart(3,'0'));
	});
	
}
