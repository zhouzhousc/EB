function clickEdit(id){
	//调用父类的属性
	parent.window.document.getElementById("podiv").style.display = "block";
	parent.window.document.getElementById("geteway_popup").style.display = "block";
//	parent.window.document.getElementById("pop_add").style.display = "none";
//	parent.window.document.getElementById("update").style.display = "none";
	
}
function go_sub_list(){
//	parent.parent.location.reload(); //重新加载页面
	parent.window.parent.window.document.getElementsByClassName("box")[1].click();//模拟点击事件
	// parent.location.href = "../sub_manage/Sub_Device_List.html";//让父界面跳转
	parent.location.href = "../shebei/devicelist";//让父界面跳转

}
