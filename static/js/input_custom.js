$(".select_box input").click(function(){
  var thisinput=$(this);
  var thisul=$(this).parent().find("ul");
  if(thisul.css("display")=="none"){
   if(thisul.height()>200){thisul.css({height:"200"+"px","overflow-y":"scroll" })};
   thisul.fadeIn("100");
   thisul.hover(function(){},function(){thisul.fadeOut("100");})
   thisul.find("li").click(function(){
   		thisinput.val($(this).text());
	   	thisul.fadeOut("100");
//	   	var value = $(this).text();
//	   	if(value == "RS232接口类"){
//			$(".myselect").css("color","");
//			$(".myselect").val("请选择协议名称");
//	   		$("#rs232").css("display","block");
//	   		$("#intel").css("display","none");
//	   		$("#other").css("display","none");
//	   	}else if(value == "以太网类型"){
//			$(".myselect").css("color","");
//			$(".myselect").val("请选择协议名称");
//	   		$("#rs232").css("display","none");
//	   		$("#intel").css("display","block");
//	   		$("#other").css("display","none");
//	   	}else if(value == "专有类型"){
//			$(".myselect").css("color","");
//			$(".myselect").val("请选择协议名称");
//	   		$("#rs232").css("display","none");
//	   		$("#intel").css("display","none");
//	   		$("#other").css("display","block");
//	   	}else{
			$(".acq_costom").css("color","#333333");
//	   	}
	   	
   }).hover(function(){$(this).addClass("hover");},function(){$(this).removeClass("hover");});
  }else{
   thisul.fadeOut("fast");
  }
 });