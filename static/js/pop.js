var sub_flag = [];
window.document.execCommand('RespectVisibilityInDesign',false,true);
$(function(){

  //判断浏览器是否支持placeholder属性
  supportPlaceholder='placeholder'in document.createElement('input'),

  placeholder=function(input){

    var text = input.attr('placeholder'),
    defaultValue = input.defaultValue;

    if(!defaultValue){

      input.val(text).addClass("phcolor");
    }

    input.focus(function(){

      if(input.val() == text){

        $(this).val("");
      }
    });


    input.blur(function(){

      if(input.val() == ""){

        $(this).val(text).addClass("phcolor");
      }
    });

    //输入的字符不为灰色
    input.keydown(function(){

      $(this).removeClass("phcolor");
    });
  };

  //当浏览器不支持placeholder属性时，调用placeholder函数
  if(!supportPlaceholder){

    $('input').each(function(){

      text = $(this).attr("placeholder");

      if($(this).attr("type") == "text"){

        placeholder($(this));
      }
    });
  }

});


function pop_close(id){
	document.getElementById(id).style.display = "none";
	document.getElementById("podiv").style.display = "none";
}
function pop_save(id){
	if(id == "update"){
		subdevice_id=document.getElementById("subdevice_name").getAttribute("name");
		subdevice_name=document.getElementById("subdevice_name").value;
		subdevice_model=document.getElementById("subdevice_model").value;
		subdevice_position=document.getElementById("subdevice_position").value;
		subdevice_remark=document.getElementById("subdevice_remark").value;
		subdevice_type=document.getElementById("subdevice_type").value;
		// console.log(subdevice_id);

		var csrf = $('input[name="csrfmiddlewaretoken"]').val();
        // 组织参数
        var params = {	'subdevice_id':subdevice_id,
			   	      	'subdevice_name':subdevice_name,
			   			'subdevice_model':subdevice_model,
						'subdevice_position':subdevice_position,
						'subdevice_remark':subdevice_remark,
						'subdevice_type':subdevice_type,
						'csrfmiddlewaretoken':csrf };
        // 设置ajax 请求为同步
        $.ajaxSettings.async = false;
        // 发起ajax post请求，访问/shebei/modify/, 传递参数:
        $.post('/shebei/modify/', params, function (data) {
            if (data.res == 2){
                // 更新成功
                console.log("修改"+data.message);
            }
            else{
                // 更新失败
                console.log(data.errmsg);
            }
        })
        // 设置ajax请求为异步, false 代表为 同步 true 代表异步
        $.ajaxSettings.async = true;
        setTimeout("window.location.reload();","500");  //2000毫秒后执行test()函数，只执行一次

		var forwarding_name = $(".forwarding_name");
		var name_val = forwarding_name.eq(0).val();
		for(var i = 1 ; i < $(".forwarding_name").length ; i++){
			forwarding_name.eq(i).text(name_val);
		}
		// console.log(name);
		
		$("#sub_iframe").contents().find("#test").css('color','red'); 


		// 模拟点击事件
		// parent.window.document.getElementsByClassName("menu")[3].click();//模拟点击事件
		// setTimeout("document.getElementsByClassName(\"menu\")[3].click()","2000");  //2000毫秒后执行test()函数，只执行一次
		// document.getElementsByClassName("menu")[3].click()
//		var tr = "<tr class='data_tr'><td>" + (i+1) +"</td><td><p class='data_name'>test_" + (i+1) +"</p></td><td><div class='data_button_div'><div class='data_enable_content'><span class='data_enable_span'>启用</span></div><div class='data_enable_button' onclick='data_clickEnable(className,"+ i +")'><div class='data_button_on'>ON</div><div class='data_button_off'>OFF</div><div class='data_button_circular'></div></div></div></td><td>10</td><td>" + time.getFullYear()+'-'+month+'-'+date+' '+hour+':'+minu+':'+secon + "</td><td>数据转发至FII CorePro</td><td style='position: relative;'><div class='data_details div_cursor' onclick='data_details(" + i + ")'>详情</div><div class='data_edit div_cursor' onclick='data_click_edit(" + i + ")'>编辑</div><div class='data_delete div_cursor' onclick='data_delete()'>删除</div></td></tr>"
//		var thead = $("#thead");
//		$(tr).insertAfter(thead);
	}
	
	if(id == "data_edit_podiv"){
		transmit_id=document.getElementById("edit_transmit_name").getAttribute("transmit_id");
		transmit_name=document.getElementById("edit_transmit_name").value;
		transmit_type=document.getElementById("edit_transmit_type").value;
		transmit_remark=document.getElementById("edit_transmit_remark").value;
		transmit_ip=document.getElementById("edit_transmit_ip").value;
		transmit_port=document.getElementById("edit_transmit_port").value;
		transmit_username=document.getElementById("edit_transmit_username").value;
		transmit_password=document.getElementById("edit_transmit_password").value;
		transmit_topic=document.getElementById("edit_transmit_topic").value;

		var csrf = $('input[name="csrfmiddlewaretoken"]').val();
        // 组织参数
        var params = {	'transmit_id':transmit_id,
			   	      	'transmit_name':transmit_name,
			   			'transmit_type':transmit_type,
						'transmit_remark':transmit_remark,
						'transmit_ip':transmit_ip,
						'transmit_port':transmit_port,
						'transmit_username':transmit_username,
						'transmit_password':transmit_password,
						'transmit_topic':transmit_topic,
						'csrfmiddlewaretoken':csrf };
        // 设置ajax 请求为同步
        $.ajaxSettings.async = false;
        // 发起ajax post请求，访问/shebei/modify/, 传递参数:
        $.post('/shebei/transmit/modify', params, function (data) {
            if (data.res == 2){
                // 更新成功
                console.log("修改"+data.message);
            }
            else{
                // 更新失败
                console.log(data.errmsg);
            }
        })
        // 设置ajax请求为异步, false 代表为 同步 true 代表异步
        $.ajaxSettings.async = true;
        setTimeout("window.location.reload();","500");  //2000毫秒后执行test()函数，只执行一次
	}
	document.getElementById(id).style.display = "none";
	document.getElementById("podiv").style.display = "none";
}

function radioClick(boo){
	if(boo == true){
		$("#forwarding_ip").text("鉴权URL：");
		$("#forwarding_port").text("DeviceName：");
		$("#forwarding_userName").text("DeviceSecret：");
		$("#forwarding_password").text("ProductKey：");
		$("#forwarding_ip").attr("id","forwarding_url");
		$("#forwarding_port").attr("id","forwarding_deviceName");
		$("#forwarding_userName").attr("id","forwarding_deviceSecret");
		$("#forwarding_password").attr("id","forwarding_productKey");
	}else{
		$("#forwarding_url").text("IP：");
		$("#forwarding_deviceName").text("端口号：");
		$("#forwarding_deviceSecret").text("User Name：");
		$("#forwarding_productKey").text("Password：");
		$("#forwarding_url").attr("id","forwarding_ip");
		$("#forwarding_deviceName").attr("id","forwarding_port");
		$("#forwarding_deviceSecret").attr("aid","forwarding_userName");
		$("#forwarding_productKey").attr("id","forwarding_password");
	}
}

function radioClick_update(boo){
	if(boo == true){
		$("#forwarding_update_ip").text("鉴权URL：");
		$("#forwarding_update_port").text("DeviceName：");
		$("#forwarding_update_userName").text("DeviceSecret：");
		$("#forwarding_update_password").text("ProductKey：");
		$("#forwarding_update_ip").attr("id","forwarding_update_url");
		$("#forwarding_update_port").attr("id","forwarding_update_deviceName");
		$("#forwarding_update_userName").attr("id","forwarding_update_deviceSecret");
		$("#forwarding_update_password").attr("id","forwarding_update_productKey");
	}else{
		$("#forwarding_update_url").text("IP：");
		$("#forwarding_update_deviceName").text("端口号：");
		$("#forwarding_update_deviceSecret").text("User Name：");
		$("#forwarding_update_productKey").text("Password：");
		$("#forwarding_update_url").attr("id","forwarding_update_ip");
		$("#forwarding_update_deviceName").attr("id","forwarding_update_port");
		$("#forwarding_update_deviceSecret").attr("aid","forwarding_update_userName");
		$("#forwarding_update_productKey").attr("id","forwarding_update_password");
	}
}

function delete_list(obj){
	console.log("aaa");
	$("#podiv").css("display","block");
	$("#pop_delete").css("display","block");
	$("#list_delete_submit").click(function (){
		if(obj != null){
			var index = $(obj).parents("tr").index()-1;
			$(obj).parents("tr").remove();
			sub_flag.splice(index,1);
			obj = null;
		}
	});
}

function pop_delete_none(obj){
	$("#pop_delete").css("display","none");
}


function delete_parent(obj){
	$("#podiv",parent.window.document).css("display","block");
	$("#pop_delete",parent.window.document).css("display","block");



	$("#list_delete_submit",parent.window.document).click(function (){
		if(obj != null){
			if(sub_flag == null){
				for(var num = 0 ; num < $("table tr").length - 1 ; num++){
					sub_flag[num] = true;
				}
			}
			var index = $(obj).parents("tr").index()-1;
			$(obj).parents("tr").remove();
			sub_flag.splice(index,1);
			obj = null;
		}
	});
}

function delete_batch(){
	$("#podiv").css("display","block");
	$("#pop_delete_batch").css("display","block");
}



function pop_delete(obj){
	$("#pop_delete").css("display","none");
	$("#podiv").css("display","none");
	$("#podiv_tips").css("display","block");
	$("#dele").css("display","block");

	$("#dele").stop(true.false).animate({
		    opacity: 1
		}, 1000,function (){
			$("#dele").animate({
	        	opacity: 0
	   		}, 3000,function (){
				$("#podiv_tips").css("display","none");
				$("#dele").css("display","none");
	   		 });
		});
}

function pop_delete_content(frame){
	$("#podiv").css("display","none");
	$("#pop_delete").css("display","none");
	var tips = $(window.frames[frame].document).find("#podiv_tips");
	var dele = $(window.frames[frame].document).find("#dele");
	var mana = $(window.frames[frame].document).find("#mana");
	mana.stop(true,true);
	tips.css("display","block");
	dele.css("display","block");
	dele.stop(true,false).animate({
		    opacity: 1
		}, 1000,function (){
			dele.animate({
	        	opacity: 0
	   		}, 3000,function (){
				dele.css("display","none");
	   		 });
		});
}

function pop_delete_batch(className){


	var election = $("."+className);
	for( var i = 0 ; i < election.length ; i++ ){
		if(election.eq(i).is(":checked")){
			var index = election.eq(i).parents("tr").index()-1;
			election.eq(i).parents("tr").remove();
			sub_flag.splice(index,1);
		}
	}


	count_num = 0;
	for(var i = 0 ; i < $(".batch").length ; i++){
		$(".batch")[i].style.backgroundColor = "";
	}
	$(".batch").hover(function(){
		this.style.cursor = "";
	});

	$("#podiv").css("display","none");
	$("#pop_delete_batch").css("display","none");
	var tips = $("#podiv_tips");
	var dele = $("#dele");
	var mana = $("#mana");
	mana.stop(true,true);
	tips.css("display","block");
	dele.css("display","block");
	dele.stop(true,false).animate({
		    opacity: 1
		}, 1000,function (){
			dele.animate({
	        	opacity: 0
	   		}, 3000,function (){
//				tips.css("display","none");
				dele.css("display","none");
	   		 });
		});
}



/*function pop_delete(id,time){
	if(time != null){
		myCount = time;
	}else{
		document.getElementById(id).style.display = "block";
		document.getElementById("podiv_tips").style.display = "block";
		document.getElementById("pop_delete").style.display = "none";
		document.getElementById("podiv").style.display = "none";
		myCount = 2;
	}
//	console.log(myCount+"秒后隐藏");
    myCount--;
	if(myCount == 0){
		id.style.display = "none";
    	document.getElementById("podiv_tips").style.display = "none";
	}
	if(myCount > 0){
   		setTimeout("pop_delete(" + id + "," + myCount + ")", 1000);
    }
//	numbe++;
//// 	console.log(num);
// 	if(numbe == 1){
//		count(2,numbe,"dele",false);
// 	}else{
// 		count(2,2);
// 	}
}*/
