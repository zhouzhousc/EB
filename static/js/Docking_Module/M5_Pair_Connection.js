var sub_flag = [];
// for(var i = 2 ; i >= 0 ; i--){
// 	sub_flag[i] = true;
// 	var tr = "<tr class='pair_tr'><td><input type='checkbox' class='pair_election_list'/></td><td>LiChuang" + i + "</td><td>USB</td><td><p>COM2</p></td><td>9600</td><td>EdgeBox对接M5</td><td style='position: relative;'><div class='button_div'><div class='enable_content'><span class='enable_span'>启用</span></div><div class='enable_button' onclick='clickEnable(this)'><div class='button_on'>ON</div><div class='button_off'>OFF</div><div class='button_circular'></div></div></div></td><td style='position: relative;'><div id='operation_div'><div id='manage' class='div_cursor' onclick='window.open(\"M5_Docking_Module_Main.html?name=1\",\"_self\")'>管理</div><div id='delete' class='div_cursor' onclick='delete_list(this)'>删除</div></div></td></tr>";
// 	var thead = $("#pair_thead");
// 	$(tr).insertAfter(thead);
// }

var baud_rate_num = 300;
for(var i = 0 ; i < 10 ; i++){
	$("#pop_pair_select").append("<option value='"+baud_rate_num+"'>"+baud_rate_num+"</option>");
	
	if(i == 7){
		baud_rate_num = 57600;
	}else{
		baud_rate_num = baud_rate_num*2;
	}
}

//function clickEnable(name,i){
//	var conName = $(".enable_span");
//	var buName = $("." + name);
//	var on = $(".button_on");
//	var off = $(".button_off");
//	var cir = $(".button_circular");
//	$("#podiv_tips").css("display","block");
//	$("#mana").css("display","block");
//	if(sub_flag[i] == true){
//		$(conName).eq(i).html("禁用");
//		$(buName).eq(i).css("background","rgba(188, 188, 188, 1)");
//		$(on).eq(i).css("display","none");
//		$(off).eq(i).css("display","block");
//		$(cir).eq(i).css("right" , "");
//		$(cir).eq(i).css("left" , "1px");
//		sub_flag[i] = false;
////	if(!$("#mana").is(":animated")){
//		$("#mana").stop(true,false).animate({
//		    opacity: 1
//		}, 1000,function (){
//			$("#mana").animate({
//	        	opacity: 0
//	   		}, 3000,function (){
//				$("#podiv_tips").css("display","none");
//				$("#mana").css("display","none");
//	   		 });
//		});
////		}
//	}else{
//		$(conName).eq(i).html("启用");
//		$(buName).eq(i).css("background","rgba(0, 159, 60, 1)");
//		$(on).eq(i).css("display","block");
//		$(off).eq(i).css("display","none");
//		$(cir).eq(i).css("right" , "1px");
//		$(cir).eq(i).css("left" , "");
//		sub_flag[i] = true;
////	if(!$("#mana").is(":animated")){
//		$("#mana").stop(true,false).animate({
//		    opacity: 1
//		}, 1000,function (){
//			$("#mana").animate({
//	        	opacity: 0
//	   		}, 3000,function (){
//				$("#podiv_tips").css("display","none");
//				$("#mana").css("display","none");
//	   		 });
//		});
////		}
//	}
//// 	console.log(num);
//
////	for(var count = 3 ; count >= 0 ; count--){
////		$("#mana")
////	}
//		
////  $("#mana").css("display","none");
////  $("#podiv_tips").css("display","none");
////  $("#mana").css("opacity","1");
//// 	if(num == 1){
////		count(2,num);
//// 	}else{
//// 		count(2,2);
//// 	}
//}




var count_num = 0;
var boo = false;
var list_length = $(".pair_election_list").length;
	//给全选按钮加上点击事件
$("#pair_selection").click(function(){
	var xz = $(this).prop("checked");//判断全选按钮的选中状态
	var ck = $(".pair_election_list").prop("checked",xz);  //让class名为qx的选项的选中状态和全选按钮的选中状态一致。
	if(xz){
		if($(".pair_election_list").length > 1){
		    for(var i = 0 ; i < $(".batch").length ; i++){
		    	$(".batch")[i].style.backgroundColor = "rgba(36, 109, 255, 1)";
		    }	
		    $(".batch").hover(function(){
		    	this.style.cursor = "pointer";
			});
			
			count_num = list_length;
			boo = true;
		}
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
$(".pair_election_list").click(function(){
    var sele = $(this).prop("checked");
	if(sele){
		count_num++;
//		console.log(count_num);
		if(count_num == list_length){
			$("#pair_selection").prop("checked","checked");
		}
	}else{
		count_num--;
		$("#pair_selection").prop("checked",false);
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