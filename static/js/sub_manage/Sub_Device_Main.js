var flagM = [true,false,false,false];
var targ = "sub_iframe";
// var website = ["Sub_Device_Information.html","Acquisition_Protocol.html","Equipment_Debugging.html","Data_Forwarding.html"];
var website = ["deviceinfo","deviceprotocol","devicededug","devicedataforward"];
var serial_slogans;
var baud_rate;
var parity_check;

var port;
var host;
function click_add(){
	$("#acq_end_tr").before("<tr class='acq_message_tr'><td><select name='cmd_id' style='width: 55%;height: 70%;background-color:transparent;'><option>03</option><option>04</option></select></td><td><input class='register_address' name='register_address' type='text' placeholder='寄存器地址' /></td><td><input class='register_address' name='register_num' type='text' placeholder='寄存器个数'  /></td><td><input class='register_address' name='register_param' type='text' placeholder='参数'  /></td><td><div class='select_div'><div id='format_box' class='format_box'>  <select id='format' name='format' class='format_box'> <option selected>Hex</option><option>Long-int</option><option>IEEE-754</option><select> </div></td><td><input class='register_address' name='rule' type='text' placeholder='公式'  /></td><td class='operation'><div id='delete' class='div_css div_cursor' onclick='delete_list(this,false)'>删除</div></td><tr/>");
}
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
function overM(className,i,n){
	document.getElementsByTagName("a")[i].href = website[i]+'/'+n;
	document.getElementsByTagName("a")[i].target = targ;
	if(i == 2){
		if(serial_slogans != null && baud_rate != null && parity_check != null){
			if(parity_check.indexOf("无校验")){
				parity_check = "n";
			}
			if(parity_check.indexOf("偶校验")){
				parity_check = "e";
			}
			if(parity_check.indexOf("奇校验")){
				parity_check = "o";
			}
	//		console.log(website[i]+"?serial_slogans="+serial_slogans+"&baud_rate="+baud_rate+"&parity_check="+parity_check);
			document.getElementsByTagName("a")[i].href = website[i]+"?serial_slogans="+serial_slogans+"&baud_rate="+baud_rate+"&parity_check="+parity_check;
		}
		if(port != null && host != null){
			document.getElementsByTagName("a")[i].href = website[i]+"?port="+port+"&host="+host;
		}
	}
}

function pop_acq_save(id){
	if(id == "config_center_modbus"){
//		console.log("modbus");
		port = null;
		host = null;
		serial_slogans = $("#acq_serial_slogans").val();
		baud_rate = $("#baud_rate").val();
		parity_check = $("#parity_check").val();
	}else if(id == "config_center_mqtt"){
//		console.log("mqtt");
		serial_slogans = null;
		baud_rate = null;
		parity_check = null;
		port = $("#port").val();
		host = $("#host").val();
	}
	document.getElementById(id).style.display = "none";
	document.getElementById("config_podiv").style.display = "none";
	document.getElementById("podiv").style.display = "none";
}
function pop_acq_apply(device_id) {
	var csrf = $('input[name="csrfmiddlewaretoken"]').val();
	var etr_name = window.document.getElementById("acq_save").getAttribute("etr_name");
	var parity_check = window.document.getElementById("parity_check").value;
	var acq_serial_slogans = window.document.getElementById("acq_serial_slogans").value;
	var data_bits = window.document.getElementById("data_bits").value;
	var baud_rate = window.document.getElementById("baud_rate").value;
	var stop_bit = window.document.getElementById("stop_bit").value;
	var time_out = window.document.getElementById("reply time out").value;
	var cycle_time = window.document.getElementById("cycle time").value;
	var code = window.document.getElementById("code").value;
	var qudong = window.document.getElementById("qudong").value;
	// console.log(etr_name,parity_check);
	// 组织参数
	var params = {	'subdevice_id':device_id,
					'etr_name':etr_name,
					'parity_check':parity_check,
					'acq_serial_slogans':acq_serial_slogans,
					'data_bits':data_bits,
					'baud_rate':baud_rate,
					'stop_bit':stop_bit,
					'time_out':time_out,
					'cycle_time':cycle_time,
					'code':code,
					'qudong':qudong,
					'csrfmiddlewaretoken':csrf };
	// 设置ajax 请求为同步
	$.ajaxSettings.async = false;
	// 发起ajax post请求，访问/cart/update, 传递参数:sku_id count
	$.post('/shebei/deviceprotocol/apply', params, function (data) {
		if (data.res == 3){
			// 更新成功
			console.log(data.message);
			document.getElementById("config_podiv").style.display = "none";
			document.getElementById("podiv").style.display = "none";
		}
		else{
			// 更新失败
			console.log(data.errmsg);

		}
		document.getElementById("config_podiv").style.display = "none";
		document.getElementById("podiv").style.display = "none";
	});
	// 设置ajax请求为异步, false 代表为 同步 true 代表异步
	$.ajaxSettings.async = true;
}

function pop_acq_close(id){
	if(id == "config_center_modbus"){
//		console.log("modbus");
	}else if(id == "config_center_mqtt"){
//		console.log("mqtt");
	}


	document.getElementById(id).style.display = "none";
	document.getElementById("config_podiv").style.display = "none";
	document.getElementById("podiv").style.display = "none";
}

// function pop_data_delete() {
// 	var transmit_id=parent.window.document.getElementById("pop_delete").getAttribute("transmit_id");
// 	console.log(id);
// 	var csrf = $('input[name="csrfmiddlewaretoken"]').val();
// 	// 组织参数
// 	var params = {'id': id,  'csrfmiddlewaretoken':csrf};
// 	// 更新购物车记录
// 	// 设置ajax 请求为同步
// 	$.ajaxSettings.async = false;
// 	// 发起ajax post请求，访问/cart/update, 传递参数:sku_id count
// 	$.post('/shebei/delete/', params, function (data) {
// 		if (data.res == 3){
// 			// 更新成功
// 			console.log("chenggong");
// 			// alert(data.message);
//
// 		}
// 		else{
// 			// 更新失败
// 			console.log("shibai");
// 			// alert(data.errmsg);
// 		}
// 	});
// 	// 设置ajax请求为异步, false 代表为 同步 true 代表异步
// 	$.ajaxSettings.async = true;
// 	console.log("aa");
// 	$("#pop_delete").css("display","none");
// 	$("#podiv").css("display","none");
// 	$("#podiv_tips").css("display","block");
// 	$("#dele").css("display","block");
// 	$("#dele").animate({
// 	    opacity: 1
// 	}, 500);
// 	$("#dele").animate({
// 	    opacity: 0
// 	}, 500);
// 	setTimeout("window.location.reload();","1000");  //2000毫秒后执行test()函数，只执行一次
// }