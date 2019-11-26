function clickEdit(id){
	//调用父类的属性
	parent.window.document.getElementById("config_center_modbus").style.display = "none";
	parent.window.document.getElementById("config_center_mqtt").style.display = "none";
	parent.window.document.getElementById("data_add_podiv").style.display = "none";
	parent.window.document.getElementById("podiv").style.display = "block";
	parent.window.document.getElementById("update").style.display = "block";
//	parent.window.document.getElementById("pop_add").style.display = "none";
	
}