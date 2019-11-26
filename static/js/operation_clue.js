var sub_flag = [];


function data_clickEnable(name){
	if(sub_flag == null){
		for(var num = 0 ; num < $("table tr").length - 1 ; num++){
			sub_flag[num] = true;
		}
	}
	var conName = $(".data_enable_span");
	var buName = $(name);
	var on = $(".data_button_on");
	var off = $(".data_button_off");
	var cir = $(".data_button_circular");
	var i = buName.parent().parent().parent().index()-1;
	
	$("#dele").stop(true,true);
	$("#podiv_tips").css("display","block");
	$("#mana").css("display","block");
	
	if(sub_flag[i] == true){
		$(conName).eq(i).html("禁用");
		$(buName).css("background-color","rgba(188, 188, 188, 1)");
		$(on).eq(i).css("display","none");
		$(off).eq(i).css("display","block");
		$(cir).eq(i).css("right" , "");
		$(cir).eq(i).css("left" , "1px");
		sub_flag[i] = false;
		
		$("#mana").stop(true,false).animate({
		    opacity: 1
		}, 1000,function (){
			$("#mana").animate({
	        	opacity: 0
	   		}, 3000,function (){
				$("#mana").css("display","none");
	   		 });
		});
	}else{
		$(conName).eq(i).html("启用");
		$(buName).css("background","rgba(0, 159, 60, 1)");
		$(on).eq(i).css("display","block");
		$(off).eq(i).css("display","none");
		$(cir).eq(i).css("right" , "1px");
		$(cir).eq(i).css("left" , "");
		sub_flag[i] = true;
		
		$("#mana").stop(true.false).animate({
		    opacity: 1
		}, 1000,function (){
			$("#mana").animate({
	        	opacity: 0
	   		}, 3000,function (){
				$("#mana").css("display","none");
	   		 });
		});
	}
}



function clickEnable(name){
	if(sub_flag == null){
		for(var num = 0 ; num < $("table tr").length - 1 ; num++){
			sub_flag[num] = true;
		}
	}
	var conName = $(".enable_span");
	var buName = $(name);
	var on = $(".button_on");
	var off = $(".button_off");
	var cir = $(".button_circular");
	var i = buName.parent().parent().parent().index()-1;
	
	$("#dele").stop(true,true);
	$("#podiv_tips").css("display","block");
	$("#mana").css("display","block");
	
	if(sub_flag[i] == true){
		$(conName).eq(i).html("禁用");
		$(buName).css("background-color","rgba(188, 188, 188, 1)");
		$(on).eq(i).css("display","none");
		$(off).eq(i).css("display","block");
		$(cir).eq(i).css("right" , "");
		$(cir).eq(i).css("left" , "1px");
		sub_flag[i] = false;
		
		$("#mana").stop(true,false).animate({
		    opacity: 1
		}, 1000,function (){
			$("#mana").animate({
	        	opacity: 0
	   		}, 3000,function (){
				$("#mana").css("display","none");
	   		 });
		});
	}else{
		$(conName).eq(i).html("启用");
		$(buName).css("background","rgba(0, 159, 60, 1)");
		$(on).eq(i).css("display","block");
		$(off).eq(i).css("display","none");
		$(cir).eq(i).css("right" , "1px");
		$(cir).eq(i).css("left" , "");
		sub_flag[i] = true;
		
		$("#mana").stop(true.false).animate({
		    opacity: 1
		}, 1000,function (){
			$("#mana").animate({
	        	opacity: 0
	   		}, 3000,function (){
				$("#mana").css("display","none");
	   		 });
		});
	}
}