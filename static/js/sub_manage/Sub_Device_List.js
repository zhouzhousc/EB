//function election(th){
//  //找到下面所有的复选框
//  var ck =document.getElementsByClassName("election_list");
//  //遍历所有复选框，设置选中状态。
//  for(var i=0;i<ck.length;i++)    {
//      if(th	.checked){//判断全选按钮的状态是不是选中的
//          ck[i].setAttribute("checked","checked");//如果是选中的，就让所有的状态为选中。
//      }else{
//          ck[i].removeAttribute("checked");//如果不是选中的，就移除所有的状态是checked的选项。
//      }
//  }
//}
// for(var i = 3 ; i >= 0 ; i--){
// 	var tr = "<tr class='tr'><td><input type='checkbox' class='election_list'/></td><td><p class='name'>"+ i+ "LiChuang</p></td><td>力创三相电表</td><td>E6-2F</td><td>JUYOUWETY</td><td>力创智能电表</td><td>2019-05-23 17:32:11.765</td><td style='position: relative;'><div class='button_div'><div class='enable_content'><span class='enable_span'>启用</span></div><div class='enable_button' onclick='clickEnable(className,"+ i +")'><div class='button_on'>ON</div><div class='button_off'>OFF</div><div class='button_circular'></div></div></div></td><td><p class='isOnLine'></p></td><td style='position: relative;'><div id='manage' class='div_cursor' onclick='window.open(\"Sub_Device_Main.html?name=1\",\"_self\")'>管理</div><div id='delete' class='div_cursor' onclick='delete_list()'>删除</div></td></tr>"
// 	var thead = $("#sub_thead");
// 	$(tr).insertAfter(thead);
// }
//var list_numbers = document.getElementsByTagName("tr").length;
//document.getElementById("list_count_span").innerHTML = list_numbers-1;

var num = 0;
var sub_flag = [];
for(var i = 0 ; i < document.getElementsByClassName("enable_button").length ; i++){
	var text=document.getElementsByClassName("enable_span")[i].innerHTML;
	console.log(text);
	if(text=="启用"){
		sub_flag[i] = true;
	}
	else {
		sub_flag[i] = false;
	}

	// if(sub_flag[i] == true){
	// 	document.getElementsByClassName("isOnLine")[i].style.color = "#00CC00";
	// 	document.getElementsByClassName("isOnLine")[i].innerText = "在线";
	// }else{
	// 	document.getElementsByClassName("isOnLine")[i].style.color = "";
	// 	document.getElementsByClassName("isOnLine")[i].innerText = "离线";
	// }
}
function open_add(){
	document.getElementById("podiv").style.display = "block";
	document.getElementById("pop_device_add").style.display = "block";
//	parent.window.parent.window.document.getElementById("pop_delete").style.display = "none";
//	parent.window.parent.window.document.getElementById("geteway_popup").style.display = "none";
//	parent.window.parent.window.document.getElementById("update").style.display = "none";
}
function clickEnable(name,i,id){
	var conName = document.getElementsByClassName("enable_span");
	var buName = document.getElementsByClassName(name);
	var on = document.getElementsByClassName("button_on");
	var off = document.getElementsByClassName("button_off");
	var cir = document.getElementsByClassName("button_circular");
	var ison = document.getElementsByClassName("isOnLine");
	document.getElementById("podiv_tips").style.display = "block";
	document.getElementById("mana").style.display = "block";
	if(sub_flag[i] == true){

		var csrf = $('input[name="csrfmiddlewaretoken"]').val();
        // 组织参数
        var params = {'device_id':id, "device_enable":0, 'csrfmiddlewaretoken':csrf};
        // 更新购物车记录
        // 设置ajax 请求为同步
        $.ajaxSettings.async = false;
        // 发起ajax post请求，访问/shebei/update, 传递参数:device_id
        $.post('/shebei/update', params, function (data) {
            if (data.res == 2){
                // 更新成功
				console.log("禁用"+data.message);
            }
            else{
                // 更新失败
				console.log(data.errmsg);

            }
        });
        // 设置ajax请求为异步, false 代表为 同步 true 代表异步
        $.ajaxSettings.async = true;

		$(conName).eq(i).html("禁用");
		$(buName).eq(i).css("background","rgba(188, 188, 188, 1)");
		$(on).eq(i).css("display","none");
		$(off).eq(i).css("display","block");
		$(cir).eq(i).css("right" , "");
		$(cir).eq(i).css("left" , "1px");
		// $(ison).eq(i).css("color","");
		// $(ison).eq(i).html("离线");
		sub_flag[i] = false;
		$("#mana").animate({
	        opacity: 1
	    }, 400);
	}else{
		var csrf = $('input[name="csrfmiddlewaretoken"]').val();
        // 组织参数
        var params = {'device_id':id, "device_enable":1, 'csrfmiddlewaretoken':csrf};
        // 更新购物车记录
        // 设置ajax 请求为同步
        $.ajaxSettings.async = false;
        // 发起ajax post请求，访问/shebei/update, 传递参数:device_id
        $.post('/shebei/update', params, function (data) {
            if (data.res == 2){
                // 更新成功
				console.log("启用"+data.message);
            }
            else{
                // 更新失败
				console.log(data.errmsg);

            }
        });
        // 设置ajax请求为异步, false 代表为 同步 true 代表异步
        $.ajaxSettings.async = true;
		$(conName).eq(i).html("启用");
		$(buName).eq(i).css("background","rgba(0, 159, 60, 1)");
		$(on).eq(i).css("display","block");
		$(off).eq(i).css("display","none");
		$(cir).eq(i).css("right" , "1px");
		$(cir).eq(i).css("left" , "");
		// $(ison).eq(i).css("color","#00CC00");
		// $(ison).eq(i).html("在线");
		sub_flag[i] = true;
		$("#mana").animate({
	        opacity: 1
	    }, 400);
	}
   	num++;
// 	console.log(num);

//	for(var count = 3 ; count >= 0 ; count--){
//		$("#mana")
//	}
	$("#mana").animate({
        opacity: 0
    }, 400);
    
//  $("#mana").css("display","none");
//  $("#podiv_tips").css("display","none");
//  $("#mana").css("opacity","1");
// 	if(num == 1){
//		count(2,num);
// 	}else{
// 		count(2,2);
// 	}
}

function pop_delete(name){

	if(name=="transmit"){
		// var id=document.getElementById("pop_delete").getAttribute("transmit_id");
		// console.log(id);
	}
	else{
		var id=document.getElementById("pop_delete").getAttribute("subdevice_id");
		console.log(id);
		var csrf = $('input[name="csrfmiddlewaretoken"]').val();
		// 组织参数
		var params = {'id': id,  'csrfmiddlewaretoken':csrf};
		// 更新购物车记录
		// 设置ajax 请求为同步
		$.ajaxSettings.async = false;
		// 发起ajax post请求，访问/cart/update, 传递参数:sku_id count
		$.post('/shebei/delete/', params, function (data) {
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

function delete_list(subdevice_id){
	// console.log(subdevice_id);
	document.getElementById("podiv").style.display = "block";
//	parent.window.parent.window.document.getElementById("gateway_Restart").style.display = "block";
//	parent.window.parent.window.document.getElementById("geteway_popup").style.display = "none";
//	parent.window.parent.window.document.getElementById("pop_delete").style.display = "none";
//	parent.window.parent.window.document.getElementById("pop_add").style.display = "none";
	document.getElementById("pop_delete").style.display = "block";
	// 添加id到删除提示
	document.getElementById("pop_delete").setAttribute("subdevice_id", subdevice_id)
}





var count_num = 0;
var boo = false;
var list_length = $(".election_list").length;
	//给全选按钮加上点击事件
$("#election").click(function(){
	var xz = $(this).prop("checked");//判断全选按钮的选中状态
	var ck = $(".election_list").prop("checked",xz);  //让class名为qx的选项的选中状态和全选按钮的选中状态一致。
	if(xz){
	    for(var i = 0 ; i < $(".batch").length ; i++){
	    	$(".batch")[i].style.backgroundColor = "rgba(36, 109, 255, 1)";
	    }	
	    $(".batch").hover(function(){
	    	this.style.cursor = "pointer";
		});
		
		count_num = list_length;
		boo = true;
	}else{
	    for(var i = 0 ; i < $(".batch").length ; i++){
	    	$(".batch")[i].style.backgroundColor = "";
	    }	
	    $(".batch").hover(function(){
	     	this.style.cursor = "";
	    });
	    
	    count_num = 0;
	    boo = false;
	}
});
$(".election_list").click(function(){
    var sele = $(this).prop("checked");
	if(sele){
		count_num++;
//		console.log(count_num);
		if(count_num == list_length){
			$("#election").prop("checked","checked");
		}
	}else{
		count_num--;
		$("#election").prop("checked",false);
	}
	if(count_num >= 2){
     	for(var i = 0 ; i < $(".batch").length ; i++){
    		$(".batch")[i].style.backgroundColor = "rgba(36, 109, 255, 1)";
     	}
	    $(".batch").hover(function(){
	     	this.style.cursor = "pointer";
		});
    }else{
	    for(var i = 0 ; i < $(".batch").length ; i++){
	    	$(".batch")[i].style.backgroundColor = "";
	    }
	    $(".batch").hover(function(){
	  		this.style.cursor = "";
		});
	}
});



/*
var pageSize = 10; //每页显示的记录条数
var curPage = 0; //当前页
var lastPage; //最后页
var direct = 0; //方向
var len; //总行数
var page; //总页数
var begin;
var end;

$(document).ready(function display() {
	len = $("#sub_tab_list tr").length - 1; // 求这个表的总行数，剔除第一行介绍
	page = len % pageSize == 0 ? len / pageSize : Math.floor(len / pageSize) + 1; //根据记录条数，计算页数
	curPage = 1; // 设置当前为第一页
	displayPage(1); //显示第一页
	$("#home_page").removeAttr("href");
	$("#pre_page").removeAttr("href");
	$("#next_page").attr("href","javascript:void(0)");
	$("#next_page").css("color","#246DFF");
	$("#tail_page").attr("href","javascript:void(0)");
	$("#tail_page").css("color","#246DFF");
	document.getElementById("page").innerHTML = "当前 " + curPage + "/" + page + " 页  "; // 显示当前多少页

	$("#home_page").click(function firstPage() { // 首页
		curPage = 1;
		direct = 0;
		$("#next_page").attr("href","javascript:void(0)");
		$("#next_page").css("color","#246DFF");
		$("#tail_page").attr("href","javascript:void(0)");
		$("#tail_page").css("color","#246DFF");
		$("#home_page").removeAttr("href");
		$("#home_page").css("color","");
		$("#pre_page").removeAttr("href");
		$("#pre_page").css("color","");
		displayPage();
	});
	$("#pre_page").click(function frontPage() { // 上一页
		direct = -1;
		$("#next_page").attr("href","javascript:void(0)");
		$("#next_page").css("color","#246DFF");
		$("#tail_page").attr("href","javascript:void(0)");
		$("#tail_page").css("color","#246DFF");
		if(curPage <= 2 && direct == -1) {
			$("#home_page").removeAttr("href");
			$("#home_page").css("color","");
			$("#pre_page").removeAttr("href");
			$("#pre_page").css("color","");
		}
		if(curPage <= 1){
			
		}else{
			displayPage();
		}
	});
	$("#next_page").click(function nextPage() { // 下一页
		direct = 1;
		$("#home_page").attr("href","javascript:void(0)");
		$("#home_page").css("color","#246DFF");
		$("#pre_page").attr("href","javascript:void(0)");
		$("#pre_page").css("color","#246DFF");
		if(curPage >= (page-1) && direct == 1) {
			$("#next_page").removeAttr("href");
			$("#next_page").css("color","");
			$("#tail_page").removeAttr("href");
			$("#tail_page").css("color","");
		}
		if(curPage >= page){
			
		}else{
			displayPage();
		}
	});
	$("#tail_page").click(function lastPage() { // 尾页
		curPage = page;
		direct = 0;
		$("#home_page").attr("href","javascript:void(0)");
		$("#home_page").css("color","#246DFF");
		$("#pre_page").attr("href","javascript:void(0)");
		$("#pre_page").css("color","#246DFF");
		$("#next_page").removeAttr("href");
		$("#next_page").css("color","");
		$("#tail_page").removeAttr("href");
		$("#tail_page").css("color","");
		displayPage();
	});
	$("#submit_paging").click(function changePage() { // 转页
		curPage = document.getElementById("page_skip").value * 1;
		if(!/^[1-9]\d*$/.test(curPage)) {
//			alert("请输入正整数");
			return;
		}
		if(curPage > page) {
//			alert("超出数据页面");
			return;
		}
		direct = 0;
		if(curPage == 1){
			$("#next_page").attr("href","javascript:void(0)");
			$("#next_page").css("color","#246DFF");
			$("#tail_page").attr("href","javascript:void(0)");
			$("#tail_page").css("color","#246DFF");
			$("#home_page").removeAttr("href");
			$("#home_page").css("color","");
			$("#pre_page").removeAttr("href");
			$("#pre_page").css("color","");
		}
		if(curPage == page){
			$("#home_page").attr("href","javascript:void(0)");
			$("#home_page").css("color","#246DFF");
			$("#pre_page").attr("href","javascript:void(0)");
			$("#pre_page").css("color","#246DFF");
			$("#next_page").removeAttr("href");
			$("#next_page").css("color","");
			$("#tail_page").removeAttr("href");
			$("#tail_page").css("color","");
		}
		displayPage();
	});

	$("#pageSizeSet").click(function setPageSize() { // 设置每页显示多少条记录
		pageSize = document.getElementById("pageSize").value; //每页显示的记录条数
		if(!/^[1-9]\d*$/.test(pageSize)) {
			alert("请输入正整数");
			return;
		}
		len = $("#mytable tr").length - 1;
		page = len % pageSize == 0 ? len / pageSize : Math.floor(len / pageSize) + 1; //根据记录条数，计算页数
		curPage = 1; //当前页
		direct = 0; //方向
		firstPage();
	});
});
	
function displayPage() {
//	if(curPage <= 1 && direct == -1) {
//		direct = 0;
//		alert("已经是第一页了");
//		return;
//	} else if(curPage >= page && direct == 1) {
//		direct = 0;
//		alert("已经是最后一页了");
//		return;
//	}

	lastPage = curPage;

	// 修复当len=1时，curPage计算得0的bug
	if(len > pageSize) {
		curPage = ((curPage + direct + len) % len);
	} else {
		curPage = 1;
	}

	document.getElementById("page").innerHTML = "当前 " + curPage + "/" + page + " 页 "; // 显示当前多少页

	begin = (curPage - 1) * pageSize + 1; // 起始记录号
	end = begin + 1 * pageSize - 1; // 末尾记录号

	if(end > len) end = len;
	$("#sub_tab_list tr").hide(); // 首先，设置这行为隐藏
	$("#sub_tab_list tr").each(function(i) { // 然后，通过条件判断决定本行是否恢复显示
		if((i >= begin && i <= end) || i == 0) //显示begin<=x<=end的记录
			$(this).show();
	});
}
*/