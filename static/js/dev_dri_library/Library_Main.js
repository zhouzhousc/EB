var flagM = [true,false];
var targ = "library_iframe";
var website = ["drive","template"];

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