//获取GET id值
get();



function get(){
    //获取当前URL
    var local_url = document.location.href;
    if(local_url.indexOf("?") >= 0){
    	$("#equ_right_tips").css("display","none");
    	$("#equ_right_modbus").css("display","none");
    	$("#equ_right_mqtt").css("display","none");
	    //截取get字符串
	    var getstr = local_url.substr(local_url.indexOf('?')+1);
	    //解析成get数组
	    var get = getstr.split('&')

	    //查找要找到参数
	    var serial_slogans = "serial_slogans";
	    var baud_rate = "baud_rate";
	    var parity_check = "parity_check";

	    var port = "port";
	    var host = "host";

	    if(getstr.indexOf(serial_slogans) >= 0){
    		$("#equ_right_modbus").css("display","block");
//  		alert(getstr);
	    }

	    if(getstr.indexOf(port) >= 0){
    		$("#equ_right_mqtt").css("display","block");
//  		alert(getstr);
	    }

	    for(var i in get){
	        if(get[i].indexOf(serial_slogans+'=')>=0){
	        	serial_slogans = get[i].replace(serial_slogans+'=','');
	        	$("#acq_serial_slogans").text(serial_slogans);
	        }
	        if(get[i].indexOf(baud_rate+'=')>=0){
	        	baud_rate = get[i].replace(baud_rate+'=','');
	        	$("#acq_baud_rate").text(baud_rate);
	        }
	        if(get[i].indexOf(parity_check+'=')>=0){
	        	parity_check = get[i].replace(parity_check+'=','');
	        	if(parity_check.indexOf("n")){
	        		parity_check = "n(无校验)";
	        	}
	        	if(parity_check.indexOf("e")){
	        		parity_check = "e(偶校验)";
	        	}
	        	if(parity_check.indexOf("o")){
	        		parity_check = "o(奇校验)";
	        	}
	        	$("#acq_parity_check").text(parity_check);
	        }

	        if(get[i].indexOf(port+'=') >= 0){
	        	port = get[i].replace(port+'=','');
	        	if(port == ""){
	        		port = "无";
	        	}
	        	$("#acq_port").text(port);
	        }
	        if(get[i].indexOf(host+'=') >= 0){
	        	host = get[i].replace(host+'=','');
	        	if(host == ""){
	        		host = "无";
	        	}
	        	$("#acq_host").text(host);
	        }
	    }
	    $("#feature_extraction > span").css("color","#FFFFFF");
	    $("#feature_extraction").css("background-color","rgba(22, 155, 213, 1)");
	    $("#feature_extraction").attr("onclick","debugging()");
    }
    //如果找不到返回false
	//  return false;
}


function go_acq_pro(){
	parent.window.document.getElementsByClassName("menu")[1].click();//模拟点击事件
	location.href = "Acquisition_Protocol.html";//让父界面跳转
}

//if($.cookie("boo") != null){
//	boo_1 = $.cookie("boo");
//	bo_1 = JSON.parse(boo_1);
//	if(boo_1 != null){
//		if(boo_1 != "null"){
//			if(bo_1.bool == true){
// 				for(var i = 10 ; i >=1 ; i--){
// 					var tr = "<tr><td><input type='checkbox' class='select_list'/></td><td>" + i + "</td><td>Temperature</td><td>28</td></tr>";
// 					var thead = $("#equ_thead");
// 					$(tr).insertAfter(thead);
// 				}
// 				$("#control_block").css("display","block");
// 				equ_page();
//			}
//		}
//	}
//}

//$(function() {
////			 if($.cookie("o") == null) {
//			   varo = { name: "张三", age: 24 };
//			   alert(varo);
//			   varstr = JSON.stringify(varo);　　//对序列化成字符串然后存入cookie
//			   alert(varstr);
//			   $.cookie("o", varstr, {
//				 expires:7 //设置时间，如果此处留空，则浏览器关闭此cookie就失效。
//			   });
////			   alert("cookie为空");
////			 }
////			 else{
////			   varstr1 = $.cookie("o");
////			   varo1 = JSON.parse(varstr1);　　//字符反序列化成对象
////			   alert(varo1.name+","+varo1.age);　　　　　　　　//输反序列化出来的对象的姓名值
////			 }
//});

function debugging(){
	$("#equ_table_tips").remove();
	for(var i = 5 ; i >=1 ; i--){
		var tr = "<tr><td><input type='checkbox' class='select_list'/></td><td>" + i + "</td><td>Temperature</td><td>28</td><td>32</td><td>20</td><td>26</td></tr>";
		var thead = $("#equ_thead");
		$(tr).insertAfter(thead);
	}
	$("#control_block").css("display","block");

	boo = { bool:true , id:1 };
//	alert(boo.bool);
	bo = JSON.stringify(boo);

//	alert(bo);
	$.cookie("boo",bo);
	equ_page();
}
function update_page_info(){
	let params= [];
	var key=$("#select_all").attr("name");
	$('.td').find(':checked').each(function () {
		params.push($(this).attr("name"));
	});

	console.log(key);
	console.log(params);
}

function click_generate(){
	// console.log(1);
	//  select_list
	$("#podiv" , document).css("display","block");
	$("#generate_template" , document).css("display","block");
}




var count_num = 0;
var boo = false;
var list_length = $(".select_list").length;



$("#equ_generate").css("background-color","rgba(36, 109, 255, 1)");
$("#equ_generate").attr("onclick","click_generate()");
$("#equ_generate").hover(function(){
	this.style.cursor = "pointer";
});

//给全选按钮加上点击事件
$("#select_all").click(function(){
	var xz = $(this).prop("checked");//判断全选按钮的选中状态
	var ck = $(".select_list").prop("checked",xz);  //让class名为select_list的选项的选中状态和全选按钮的选中状态一致。
	if(xz){
		console.log(1);
		$("#equ_generate").css("background-color","rgba(36, 109, 255, 1)");
		$("#equ_generate").attr("onclick","click_generate()");
		$("#equ_generate").hover(function(){
			this.style.cursor = "pointer";
		});

		count_num = list_length;
		boo = true;
	}else{
		console.log(0);
		$("#equ_generate").css("background-color","");
		$("#equ_generate").removeAttr("onclick");
		$("#equ_generate").hover(function(){
			this.style.cursor = "";
		});

		count_num = 0;
		boo = false;
	}
	update_page_info()
});
//给每个复选框加上点击事件 ，复选框选中两个或以上则可以点击生成模板
$(".select_list").click(function(){
	var sele = $(this).prop("checked");
	if(sele){
		count_num++;
//		console.log(count_num);
		if(count_num == list_length){
			$("#select_all").prop("checked","checked");
		}
	}else{
		count_num--;
		console.log("aa");
		$("#select_all").prop("checked",false);
	}

	if(count_num >= 1){
		$("#equ_generate").css("background-color","rgba(36, 109, 255, 1)");
		$("#equ_generate").attr("onclick","click_generate()");
		$("#equ_generate").hover(function(){
			this.style.cursor = "pointer";
		});
	}else{
		$("#equ_generate").css("background-color","");
		$("#equ_generate").removeAttr("onclick");
		$("#equ_generate").hover(function(){
			this.style.cursor = "";
		});
	}
	update_page_info()

});

//分页
function equ_page(){
	var pageSize = 10; //每页显示的记录条数
	var curPage = 0; //当前页
	var lastPage; //最后页
	var direct = 0; //方向
	var len; //总行数
	var page; //总页数
	var begin;
	var end;

	//计算总数
	var list_numbers = document.getElementsByTagName("tr").length;
	document.getElementById("equ_count_span").innerHTML = list_numbers-1;





	$(document).ready(function display() {
		len = $("#equ_table tr").length - 1; // 求这个表的总行数，剔除第一行介绍
		page = len % pageSize == 0 ? len / pageSize : Math.floor(len / pageSize) + 1; //根据记录条数，计算页数
		curPage = 1; // 设置当前为第一页
		displayPage(1); //显示第一页
		$("#home_page").removeAttr("href");
		$("#pre_page").removeAttr("href");
		if(page >= 2){
			$("#next_page").attr("href","javascript:void(0)");
			$("#next_page").css("color","#246DFF");
			$("#tail_page").attr("href","javascript:void(0)");
			$("#tail_page").css("color","#246DFF");
		}
		document.getElementById("page").innerHTML = "当前 " + curPage + "/" + page + " 页  "; // 显示当前多少页

		$("#home_page").click(function firstPage() { // 首页
			if(curPage === 1 && direct === 0){

			}else{
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
			}
		});
		$("#pre_page").click(function frontPage() { // 上一页
			if(curPage <= 1){

			}else{
				direct = -1;
				$("#next_page").attr("href","javascript:void(0)");
				$("#next_page").css("color","#246DFF");
				$("#tail_page").attr("href","javascript:void(0)");
				$("#tail_page").css("color","#246DFF");
				$("#home_page").removeAttr("href");
				$("#home_page").css("color","");
				$("#pre_page").removeAttr("href");
				$("#pre_page").css("color","");
				displayPage();
			}
		});
		$("#next_page").click(function nextPage() { // 下一页
			if(curPage < page){
				direct = 1;
				$("#home_page").attr("href","javascript:void(0)");
				$("#home_page").css("color","#246DFF");
				$("#pre_page").attr("href","javascript:void(0)");
				$("#pre_page").css("color","#246DFF");
				$("#next_page").removeAttr("href");
				$("#next_page").css("color","");
				$("#tail_page").removeAttr("href");
				$("#tail_page").css("color","");
				displayPage();
			}else{
			}
		});
		$("#tail_page").click(function lastPage() { // 尾页
			if(curPage >= page){
			}else{
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
			}
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

	//	$("#pageSizeSet").click(function setPageSize() { // 设置每页显示多少条记录
	//		pageSize = document.getElementById("pageSize").value; //每页显示的记录条数
	//		if(!/^[1-9]\d*$/.test(pageSize)) {
	//			alert("请输入正整数");
	//			return;
	//		}
	//		len = $("#mytable tr").length - 1;
	//		page = len % pageSize == 0 ? len / pageSize : Math.floor(len / pageSize) + 1; //根据记录条数，计算页数
	//		curPage = 1; //当前页
	//		direct = 0; //方向
	//		firstPage();
	//	});
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
		$("#equ_table tr").hide(); // 首先，设置这行为隐藏
		$("#equ_table tr").each(function(i) { // 然后，通过条件判断决定本行是否恢复显示
			if((i >= begin && i <= end) || i == 0) //显示begin<=x<=end的记录
				$(this).show();
		});
	}
}
