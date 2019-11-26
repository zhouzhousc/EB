var flag = [false,true,false,false,false];
var targ = "inteface_iframe";
// var website = ["gateway_manage/Gateway_Main.html","sub_manage/Sub_Device_List.html","Remote_Manage/Remote_Manage_Main.html","logging_events/Logging_Events_Main.html","dev_dri_library/Library_Main.html",""];
var website = ["../wangguang/manage","../shebei/devicelist","../yuancheng/manage","../loginfo/manage","../qudong/manage","../m5/manage"];

var result = [];
var a = document.getElementsByTagName("a");
var tag = document.getElementsByTagName("div");
for(var j = 0 ; j < tag.length ; j++){
	var clName = tag[j].className.split(" ");
	for(var b = 0 ; b < clName.length ; b++){
		if(clName[b] == "box"){
			result.push(tag[j]);
		}
	}
}
	
if(flag[0] == true){
	result[0].style.filter = "progid:DXImageTransform.Microsoft.gradient(startcolorstr=#20808080,endcolorstr=#20808080)";
	$(".list_img").eq(0).attr("src","../../static/img/gateway/gateway_manage/change/0.png");
	$(".box").eq(0).css("background","rgba(35, 46, 57, 1)");
	$(".menuList").eq(0).css("color","rgb(50,135,178)");
}else if(flag[1] == true){
	result[1].style.filter = "progid:DXImageTransform.Microsoft.gradient(startcolorstr=#20808080,endcolorstr=#20808080)";
	$(".list_img").eq(1).attr("src","../../static/img/gateway/gateway_manage/change/1.png");
	$(".box").eq(1).css("background","rgba(35, 46, 57, 1)");
	$(".menuList").eq(1).css("color","rgb(50,135,178)");
}
function changeFrameHeight(){
  var iframe= document.getElementById(targ);
  iframe.height= 0;   //这里必须要先设置成0，不然后面会有问题
  iframe.height=iframe.contentWindow.document.body.scrollHeight;
}
function clickDiv(className,i){
	if(document.getElementsByClassName){
		if(flag[i] == true){
			document.getElementsByTagName("a")[i].removeAttribute("href");
			document.getElementsByTagName("a")[i].removeAttribute("target");
		}else{
			document.getElementsByTagName("a")[i].href = website[i];
			document.getElementsByTagName("a")[i].target = targ;
		}
		for(var j = 0 ; j < result.length ; j++){
			$(".list_img").eq(j).attr("src","../../static/img/gateway/gateway_manage/" + j + ".png");
			result[j].style.background = "";
			$(".menuList").eq(j).css("color","");
			$(".menuList").eq(j).css("cursor","pointer");
			a[j].style.cursor = "pointer";
			result[j].style.cursor = "pointer";
			flag[j] = false;
		}
		flag[i] = true;
		$(".menuList").eq(i).css("color","rgb(50,135,178)");
		$(".list_img").eq(i).attr("src","../../static/img/gateway/gateway_manage/change/" + i + ".png");
		$(".menuList").eq(i).css("cursor","text");
		result[i].style.background = "rgba(35, 46, 57, 1)";
		result[i].style.cursor = "text";
		a[i].style.cursor = "text";
	}else{
		if(flag[i] == true){
			a[i].removeAttribute("href");
			a[i].removeAttribute("target");
		}else{
			a[i].href = website[i];
			a[i].target = targ;
		}
		for(var j = 0 ; j < result.length ; j++){
			result[j].style.filter = "";
			$(".menuList").eq(j).css("color","");
			$(".menuList").eq(j).css("cursor","pointer");
			$(".list_img").eq(j).attr("src","../../static/img/gateway/gateway_manage/" + j + ".png");
			a[j].style.cursor = "pointer";
			result[j].style.cursor = "pointer";
			flag[j] = false;
		}
		flag[i] = true;
		$(".list_img").eq(i).attr("src","../../static/img/gateway/gateway_manage/change/" + i + ".png");
		$(".menuList").eq(i).css("color","rgb(50,135,178)");
		$(".menuList").eq(i).css("cursor","text");
		result[i].style.filter = "progid:DXImageTransform.Microsoft.gradient(startcolorstr=#20808080,endcolorstr=#20808080)";
		result[i].style.cursor = "text";
		a[i].style.cursor = "text";
	}	
}
function over(className,i){
	
	var iframe_src = document.getElementById("inteface_iframe").src;
	if(iframe_src == "http://127.0.0.1:8020/Getaway/HTML/sub_manage/Sub_Device_List.html"){
		flag[0] = false;
		flag[1] = true;
	}
	if(document.getElementsByClassName){
		if(flag[i] == true){
			result[i].style.cursor = "text";
			$(".menuList").eq(i).css("cursor","text");
			a[i].style.cursor = "text";
		}else{
			result[i].style.cursor = "pointer";
			a[i].style.cursor = "pointer";
			$(".list_img").eq(i).attr("src","../../static/img/gateway/gateway_manage/change/" + i + ".png");
			$(".menuList").eq(i).css("color","rgb(50,135,178)");
			$(".menuList").eq(i).css("cursor","pointer");
			result[i].style.background = "rgba(35, 46, 57, 1)";
		}
		return;
	}else{
		if(flag[i] == true){
			result[i].style.cursor = "text";
			$(".menuList").eq(i).css("cursor","text");
			a[i].style.cursor = "text";
		}else{
			$(".list_img").eq(i).attr("src","../../static/img/gateway/gateway_manage/change/" + i + ".png");
			result[i].style.cursor = "pointer";
			a[i].style.cursor = "pointer";
			$(".menuList").eq(i).css("cursor","pointer");
			$(".menuList").eq(i).css("color","rgb(50,135,178)");
			result[i].style.filter = "progid:DXImageTransform.Microsoft.gradient(startcolorstr=#20808080,endcolorstr=#20808080)";
		}
		
		return;
	}
}
function out(className,i){
	if(document.getElementsByClassName){
		if(flag[i] == true){
		}else{
			result[i].style.background = "";
			$(".menuList").eq(i).css("color","");
			$(".list_img").eq(i).attr("src","../../static/img/gateway/gateway_manage/" + i + ".png");
	
		}
		return;
	}else{
		if(flag[i] == true){
		}else{
			result[i].style.filter = "";
			$(".menuList").eq(i).css("color","");
			$(".list_img").eq(i).attr("src","../../static/img/gateway/gateway_manage/" + i + ".png");
		}
		return;
	}
}

function display_edition(boo){
	if(boo == true){
		$("#edition").css("display","block");
		$("#u157_img").attr("src","../../static/img/gateway/u24_mouseOver.png");
	}else{
		$("#edition").css("display","none");
		$("#u157_img").attr("src","../../static/img/gateway/u157.png");
	}
}
