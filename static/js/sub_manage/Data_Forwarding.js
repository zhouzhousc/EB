var time = new Date();
//console.log(time.getFullYear()+"-"+time.getMonth()+"-"+time.getDate()+" "+time.getHours()+":"+time.getMinutes()+":"+time.getSeconds());
var month = time.getMonth();
var date = time.getDate()
var hour = time.getHours();
var minu = time.getMinutes();
var secon = time.getSeconds();
var sub_flag = [true,true,true,true];
for(var i = 0 ; i < document.getElementsByClassName("data_enable_button").length ; i++) {
	var text = document.getElementsByClassName("data_enable_span")[i].innerHTML;
	console.log(text);
	if (text == "启动") {
		sub_flag[i] = true;
	} else {
		sub_flag[i] = false;

	}
}
if(month < 10){
	month = "0" + month;
}
if(date < 10){
	date = "0" + date;
}
if(hour < 10){
	hour = "0" + hour;
}
if(minu < 10){
	minu = "0" + minu;
}
if(secon < 10){
	secon = "0" + secon;
}
// for(var i = 8 ; i >= 0 ; i--){
// 	sub_flag[i] = true;
// 	var tr = "<tr class='data_tr'><td>" + (i+1) +"</td><td><p class='data_name'>test_" + (i+1) +"</p></td><td><div class='data_button_div'><div class='data_enable_content'><span class='data_enable_span'>启用</span></div><div class='data_enable_button' onclick='data_clickEnable(className,"+ i +")'><div class='data_button_on'>ON</div><div class='data_button_off'>OFF</div><div class='data_button_circular'></div></div></div></td><td>10</td><td>" + time.getFullYear()+'-'+month+'-'+date+' '+hour+':'+minu+':'+secon + "</td><td>数据转发至FII CorePro</td><td style='position: relative;'><div class='data_details div_cursor' onclick='data_details(" + i + ")'>详情</div><div class='data_edit div_cursor' onclick='data_click_edit(" + i + ")'>编辑</div><div class='data_delete div_cursor' onclick='data_delete()'>删除</div></td></tr>"
// 	var thead = $("#data_thead");
// 	$(tr).insertAfter(thead);
// }

function data_clickEnable(name,i, transmit_id , subdevice_id, transmit_type){
	// console.log(sub_flag);
	var conName = document.getElementsByClassName("data_enable_span");
	var buName = document.getElementsByClassName(name);
	// var enable = document.getElementById("count");
	// var enable = document.getElementsByClassName("count");
	var on = document.getElementsByClassName("data_button_on");
	var off = document.getElementsByClassName("data_button_off");
	var cir = document.getElementsByClassName("data_button_circular");
	// parent.window.document.getElementById("mana").style.display = "block";
	document.getElementById("podiv_tips").style.display = "block";
	document.getElementById("mana").style.display = "block";
	if(sub_flag[i] == true){

		var csrf = $('input[name="csrfmiddlewaretoken"]').val();
        // 组织参数
        var params = {'transmit_id':transmit_id , "subdevice_id":subdevice_id,"transmit_type":transmit_type ,"transmit_enable": 0, 'csrfmiddlewaretoken':csrf};
        // 更新购物车记录
        // 设置ajax 请求为同步
        $.ajaxSettings.async = false;
        // 发起ajax post请求，访问/shebei/transmit/update, 传递参数:transmit_id
        $.post('/shebei/transmit/update', params, function (data) {
            if (data.res == 3){
                // 更新成功
				// enable.setAttribute("enable",data.transmit_enable);
				// console.log( $("#count").val());
				document.getElementsByClassName("count")[i].setAttribute("transmit_enable","0");
				document.getElementsByClassName("status")[i].innerHTML="转发停止";
				console.log("禁用"+data.message+data.transmit_enable);
				$(conName).eq(i).html("关闭");
                $(buName).eq(i).css("background","rgba(188, 188, 188, 1)");
                $(on).eq(i).css("display","none");
                $(off).eq(i).css("display","block");
                $(cir).eq(i).css("right" , "");
                $(cir).eq(i).css("left" , "1px");
                sub_flag[i] = false;
                $("#mana").animate({
                    opacity: 1
                }, 400);
                $("#mana").animate({
                opacity: 0
                }, 400);
            }
            else{
                // 更新失败
				console.log(data.errmsg);

            }
        });
        // 设置ajax请求为异步, false 代表为 同步 true 代表异步
        $.ajaxSettings.async = true;





	}else
	{	var csrf = $('input[name="csrfmiddlewaretoken"]').val();
        // 组织参数
        var params = {'transmit_id':transmit_id, "subdevice_id":subdevice_id, "transmit_type":transmit_type ,"transmit_enable":1, 'csrfmiddlewaretoken':csrf};
        // 更新购物车记录
        // 设置ajax 请求为同步
        $.ajaxSettings.async = false;
        // 发起ajax post请求，访问/shebei/transmit/update, 传递参数:transmit_id
        $.post('/shebei/transmit/update', params, function (data) {
            if (data.res == 3){
                // 更新成功
				// enable.setAttribute("enable",data.transmit_enable);
				document.getElementsByClassName("count")[i].setAttribute("transmit_enable","1");
				console.log("启用"+data.message+data.transmit_enable);
				$(conName).eq(i).html("启动");
                $(buName).eq(i).css("background","rgba(0, 159, 60, 1)");
                $(on).eq(i).css("display","block");
                $(off).eq(i).css("display","none");
                $(cir).eq(i).css("right" , "1px");
                $(cir).eq(i).css("left" , "");
                sub_flag[i] = true;
                $("#mana").animate({
                opacity: 1
                }, 400);
                $("#mana").animate({
                opacity: 0
                }, 400);
            }
            else{
                // 更新失败
				console.log(data.errmsg);

            }
        });
        // 设置ajax请求为异步, false 代表为 同步 true 代表异步
        $.ajaxSettings.async = true;


	}


	// 循环发送消息
    //     var csrf = $('input[name="csrfmiddlewaretoken"]').val();
    //     // 组织参数
    //     var params = {'transmit_id':transmit_id , "subdevice_id":subdevice_id, 'csrfmiddlewaretoken':csrf};
    //     // 更新购物车记录
    //     // 设置ajax 请求为同步
    //     $.ajaxSettings.async = false;
    //     // 发起ajax post请求，访问/shebei/transmit/update, 传递参数:transmit_id
    //     $.post('/qudong/run/', params, function (data) {
    //         if (data.res == 2){
    //             // 更新成功
	// 			console.log("禁用"+data.message);
    //         }
    //         else{
    //             // 更新失败
	// 			console.log(data.message);
    //
    //         }
    //     });
    //     // 设置ajax请求为异步, false 代表为 同步 true 代表异步
    //     $.ajaxSettings.async = true;
//	document.getElementById("podiv_tips").style.display = "block";
//	document.getElementById("mana").style.display = "block";
}

function clickAdd(id){
//	parent.window.document.getElementById("config_podiv").style.display = "none";
//	parent.window.document.getElementById("config_center_modbus").style.display = "none";
//	parent.window.document.getElementById("config_center_mqtt").style.display = "none";
//	parent.window.document.getElementById("data_add_podiv").style.display = "none";
//	parent.window.document.getElementById("update").style.display = "none";
	
	// parent.window.document.getElementById("podiv").style.display = "block";
	document.getElementById("podiv").style.display = "block";
	// parent.window.document.getElementById(id).style.display = "block";
	document.getElementById(id).style.display = "block";
}
function data_details(transmit_name, transmit_type, transmit_topic){
	console.log(transmit_name);
	console.log(transmit_topic);
	console.log(transmit_type);
	// parent.window.document.getElementById("data_details").setAttribute("transmit_id", transmit_id);
	// parent.window.document.getElementById("podiv").style.display = "block";
	document.getElementById("podiv").style.display = "block";
	// parent.window.document.getElementById("data_details").style.display = "block";
	document.getElementById("data_details").style.display = "block";
	// parent.window.document.getElementById("transmit_name").setAttribute("value", transmit_name);
	document.getElementById("transmit_name").setAttribute("value", transmit_name);
	// parent.window.document.getElementById("transmit_type").setAttribute("value", transmit_type_dict[index]);
	document.getElementById("transmit_type").setAttribute("value", transmit_type);
	// parent.window.document.getElementById("transmit_topic").setAttribute("value", transmit_topic);
	document.getElementById("transmit_topic").setAttribute("value", transmit_topic);
}
function data_click_edit(transmit_id,transmit_name, transmit_type,transmit_ip,transmit_port,transmit_username,transmit_password, transmit_topic, transmit_type_dict,transmit_remark){
	index=parseInt(transmit_type);
	console.log(transmit_name, transmit_type,transmit_ip,transmit_port,transmit_username,transmit_password, transmit_topic, transmit_type_dict,transmit_remark);
	// parent.window.document.getElementById("podiv").style.display = "block";
	document.getElementById("podiv").style.display = "block";
	// parent.window.document.getElementById("data_edit_podiv").style.display = "block";
	document.getElementById("data_edit_podiv").style.display = "block";
	document.getElementById("edit_transmit_name").setAttribute("value", transmit_name);
	document.getElementById("edit_transmit_name").setAttribute("transmit_id", transmit_id);
	// document.getElementById("edit_transmit_type").setAttribute("value", transmit_type_dict[index]);
	$("#edit_transmit_type").val(index);
	document.getElementById("edit_transmit_ip").setAttribute("value", transmit_ip);
	document.getElementById("edit_transmit_port").setAttribute("value", transmit_port);
	document.getElementById("edit_transmit_username").setAttribute("value", transmit_username);
	document.getElementById("edit_transmit_password").setAttribute("value", transmit_password);
	document.getElementById("edit_transmit_topic").setAttribute("value", transmit_topic);
	document.getElementById("edit_transmit_remark").setAttribute("value", transmit_remark);
}

function data_delete(transimt_id) {
	// parent.window.document.getElementById("podiv").style.display = "block";
	document.getElementById("podiv").style.display = "block";
	// parent.window.document.getElementById("pop_delete").style.display = "block";
	document.getElementById("pop_delete").style.display = "block";
	// 添加id到删除提示
	// parent.window.document.getElementById("pop_delete").setAttribute("transmit_id", transimt_id)
	document.getElementById("pop_delete").setAttribute("transmit_id", transimt_id)
}
function pop_data_delete(name) {
	if(name=="transmit"){
		var id=document.getElementById("pop_delete").getAttribute("transmit_id");
		console.log(id);
		var csrf = $('input[name="csrfmiddlewaretoken"]').val();
		// 组织参数
		var params = {'transmit_id': id,  'csrfmiddlewaretoken':csrf};
		// 更新购物车记录
		// 设置ajax 请求为同步
		$.ajaxSettings.async = false;
		// 发起ajax post请求，访问/cart/update, 传递参数:sku_id count
		$.post('/shebei/transmit/delete', params, function (data) {
			if (data.res == 3){
				// 更新成功
				console.log("chenggong");
				// alert(data.message);

			}
			else{
				// 更新失败
				console.log("shibai");
				// alert(data.errmsg);
			}
		});
		// 设置ajax请求为异步, false 代表为 同步 true 代表异步
		$.ajaxSettings.async = true;
		console.log("aa");
		$("#pop_delete").css("display","none");
		$("#podiv").css("display","none");
		$("#podiv_tips").css("display","block");
		$("#dele").css("display","block");
		$("#dele").animate({
			opacity: 1
		}, 500);
		$("#dele").animate({
			opacity: 0
		}, 500);
		setTimeout("window.location.reload();","1000");  //2000毫秒后执行test()函数，只执行一次
	}
}
