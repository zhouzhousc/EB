var flag = [true,false,false];
document.getElementsByClassName("menu")[0].style.background = "rgba(36, 109, 255, 1)";
document.getElementsByClassName("menu")[0].style.color = "#FFFFFF";
var tip = [["网关信息","系统信息","网关服务"],["设备信息","采集协议","特征提取","数据转发"],["配置下发","远程管理"],["日志中心","事件中心","通知管理"],["驱动库","模板库"],[]];

function clickDiv(className,i,num){
	var name = document.getElementsByClassName(className);
	for(var j = 0 ; j < name.length ; j++){
		name[j].style.color = "";
		name[j].style.background = "";
		flag[j] = false;
	}
	$("#log_sub_title").text(tip[num][i]);
	flag[i] = true;
	name[i].style.cursor = "text";
	name[i].style.color = "#FFFFFF";
	name[i].style.background = "rgba(36, 109, 255, 1)";
}
function over(className,i){
	var name = document.getElementsByClassName(className);
	if(flag[i] == true){
		name[i].style.cursor = "text";
	}else{
		for(var j = 0 ; j < name.length ; j++){
			name[j].style.cursor = "pointer";
		}
		name[i].style.color = "rgb(36, 109, 255)";
	}
}
function out(className,i){
	var name = document.getElementsByClassName(className);
	if(flag[i] == true){
	}else{
		name[i].style.color = "";
	}
}
