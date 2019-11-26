var flag = [true,false,false,false,false];
var targ = "inteface_iframe";
var website = ["gateway_manage/Gateway_Main.html","sub_manage/Sub_Device_List.html","Remote_Manage.html","logging_events/Logging_Events_Main.html","Dev_Dri_Library.html"];
$(".log_top_tittle").eq(0).css("color","rgb(36, 109, 255)");
$(".log_top_tittle").eq(0).css("border-bottom","3px solid rgb(36, 109, 255)");	
function log_center_tittle_click(classname,i){
	var clName = $("."+classname);
	for(var j = 0 ; j < flag.length ; j++){
		clName.eq(j).css("color","");
		clName.eq(j).css("border-bottom","");
	}
	clName.eq(i).css("color","rgb(36, 109, 255)");
	clName.eq(i).css("border-bottom","3px solid rgb(36, 109, 255)");
}








var pageSize = 10; //每页显示的记录条数
var curPage = 0; //当前页
var lastPage; //最后页
var direct = 0; //方向
var len; //总行数
var page; //总页数
var begin;
var end;

var list_numbers = document.getElementsByTagName("tr").length;
document.getElementById("list_count_span").innerHTML = list_numbers-1;

$(document).ready(function display() {
	len = $("#log_center_bottom_table tr").length - 1; // 求这个表的总行数，剔除第一行介绍
	page = len % pageSize == 0 ? len / pageSize : Math.floor(len / pageSize) + 1; //根据记录条数，计算页数
	curPage = 1; // 设置当前为第一页
	displayPage(1); //显示第一页
	$("#home_page").removeAttr("href");
	$("#pre_page").removeAttr("href");
	if(page > 1){
		$("#next_page").attr("href","javascript:void(0)");
		$("#next_page").css("color","#246DFF");
		$("#tail_page").attr("href","javascript:void(0)");
		$("#tail_page").css("color","#246DFF");
	}
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
	$("#log_center_bottom_table tr").hide(); // 首先，设置这行为隐藏
	$("#log_center_bottom_table tr").each(function(i) { // 然后，通过条件判断决定本行是否恢复显示
		if((i >= begin && i <= end) || i == 0) //显示begin<=x<=end的记录
			$(this).show();
	});
}