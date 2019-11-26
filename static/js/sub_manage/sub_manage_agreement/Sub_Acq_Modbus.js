var baud_rate_num = 300;
for(var i = 0 ; i < 10 ; i++){
	$("#baud_rate").append("<option value='"+baud_rate_num+"'>"+baud_rate_num+"</option>");
	
	if(i == 7){
		baud_rate_num = 57600;
	}else{
		baud_rate_num = baud_rate_num*2;
	}
}
for(var i = 0 ; i < 3 ; i++){
	$("#stop_bit").append("<option value='"+i+"'>"+i+"</option>");
}
for(var i = 5 ; i < 9 ; i++){
	$("#data_bits").append("<option value='"+i+"'>"+i+"</option>");
}
for(var i = 0 ; i < 1 ; i++){
    $("#acq_end_tr").before("<tr class='acq_message_tr'><td><select name='cmd_id' style='width: 55%;height: 70%;background-color:transparent;'><option>03</option><option>04</option></select></td><td><input class='register_address' name='register_address' type='text' placeholder='寄存器地址' /></td><td><input class='register_address' name='register_num' type='text' placeholder='寄存器个数'  /></td><td><input class='register_address' name='register_param' type='text' placeholder='参数'  /></td><td><div class='select_div'><div id='format_box' class='format_box'>  <select id='format' name='format' class='format_box'> <option selected>Hex</option><option>Long-int</option><option>IEEE-754</option><select> </div></td><td><input class='register_address' name='rule' type='text' placeholder='公式'  /></td><td class='operation'><div id='delete' class='div_css div_cursor' onclick='delete_list(this,false)'>删除</div></td><tr/>");
}

function onAddTR(trObj){
    $(trObj).after("<tr onclick='onAddTR(this)'><td>这是新行</td><td></td><tr/>");
}



 $(".format_box input").click(function(){
  var thisinput=$(this);
  var thisul=$(this).parent().find("ul");
  if(thisul.css("display")=="none"){
   if(thisul.height()>200){thisul.css({height:"200"+"px","overflow-y":"scroll" })};
   thisul.fadeIn("100");
   thisul.hover(function(){},function(){thisul.fadeOut("100");})
   thisul.find("li").click(function(){
   		thisinput.val($(this).text());
	   	thisul.fadeOut("100");
   }).hover(function(){$(this).addClass("hover");},function(){$(this).removeClass("hover");});
  }else{
   thisul.fadeOut("fast");
  }
 });