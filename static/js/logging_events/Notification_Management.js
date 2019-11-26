var sub_flag = [];
for(var i = 0 ; i < $(".notification_enable_button").length ; i++){
	sub_flag[i] = true;
}
function notification_clickEnable(name,i){
	var conName = $(".notification_enable_span");
	var buName = $("."+name);
	var on = $(".notification_button_on");
	var off = $(".notification_button_off");
	var cir = $(".notification_button_circular");
	if(sub_flag[i] == true){
		$(conName).eq(i).html("禁用");
		$(buName).eq(i).css("background","rgba(188, 188, 188, 1)");
		$(on).eq(i).css("display","none");
		$(off).eq(i).css("display","block");
		$(cir).eq(i).css("right" , "");
		$(cir).eq(i).css("left" , "1px");
		sub_flag[i] = false;
	}else{
		$(conName).eq(i).html("启用");
		$(buName).eq(i).css("background","rgba(0, 159, 60, 1)");
		$(on).eq(i).css("display","block");
		$(off).eq(i).css("display","none");
		$(cir).eq(i).css("right" , "1px");
		$(cir).eq(i).css("left" , "");
		sub_flag[i] = true;
	}
}

function notification_details(id,notice_leader,notice_phone,notice_email,notice_location){
	parent.window.document.getElementById("podiv").style.display = "block";
	parent.window.document.getElementById(id).style.display = "block";
	parent.window.document.getElementById("person").setAttribute("value", notice_leader);
	// parent.window.document.getElementById("notice_phone").setAttribute("value", notice_phone);
	parent.window.document.getElementById("phone").setAttribute("value", notice_phone);
	parent.window.document.getElementById("mail").setAttribute("value", notice_email);
	parent.window.document.getElementById("pos").setAttribute("value", notice_location);
	// document.getElementById("notice_phone").setAttribute("value", notice_phone);
}




function notification_delete(id,obj){
    // document.getElementById("podiv").style.display = "block";
    // document.getElementById("pop_delete").style.display = "block";
    // document.getElementById("pop_delete").setAttribute("value", id)
	var csrf = $('input[name="csrfmiddlewaretoken"]').val();
	var params = {
		'id':id ,
		'csrfmiddlewaretoken':csrf};

	 $.ajaxSettings.async = false;
        // 发起ajax post请求，访问/loginfo/delete, 传递参数:id
        $.post('/loginfo/delete', params, function (data) {
        	console.log(data);
            if (data.res == 3){
                // 更新成功
				// enable.setAttribute("enable",data.transmit_enable);
				console.log(data.message);

            }
            else{
                // 更新失败
				console.log(data.errmsg);

            }
        });
        // 设置ajax请求为异步, false 代表为 同步 true 代表异步
        $.ajaxSettings.async = true;


	console.log("aaa");
    $(obj).parents("tr").remove();
	// parent.window.document.getElementById("podiv").style.display = "block";
	// parent.window.document.getElementById(id).style.display = "block";
	// parent.window.document.getElementById("pos").setAttribute("value", notice_location);
	// parent.window.document.getElementById("pop_delete").setAttribute("transmit_id", transimt_id)
	// document.getElementById("notice_phone").setAttribute("value", notice_phone);
}
