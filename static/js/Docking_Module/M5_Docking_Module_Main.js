var flagM = [true,false];
var targ = "docking_iframe";
var website = ["devicedebug","devicedataforward"];

function clickM(className,i){
	if(flagM[i] == true){
		document.getElementsByTagName("a")[i].removeAttribute("href");
		document.getElementsByTagName("a")[i].removeAttribute("target");
	}
	var name = document.getElementsByClassName(className);
	for(var j = 0 ; j < name.length ; j++){
		flagM[j] = false;
	}
	flagM[i] == true;
}
function overM(className,i, m5device_name){
	document.getElementsByTagName("a")[i].href = website[i]+"/"+m5device_name;
	document.getElementsByTagName("a")[i].target = targ;
}