var flagM = [true,false,false];
var targ = "gateway_iframe";
// var website = ["Gateway_information.html","System_information.html","Initiated_Service.html"];
var website = ["info","sysinfo","service"];

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
function overM(className,i){
	document.getElementsByTagName("a")[i].href = website[i];
	document.getElementsByTagName("a")[i].target = targ;
}