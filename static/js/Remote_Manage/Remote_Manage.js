var isClick = [true,false,false];

for(var i = 0 ; i < isClick.length ; i++){
	if(isClick[i] == true){
		$(".type_select").eq(i).css("color","#246DFF");
		$(".type_select").eq(i).css("border-bottom","5px solid #246DFF");
	}
}


$(".type_select").click(function(){
	var index = $(".type_select").index(this);
	for(var i = 0 ; i < isClick.length ; i++){
		$(".type_select").eq(i).css("color","");
		$(".type_select").eq(i).css("border-bottom","");
		isClick[i] = false;
	}
	$(".type_select").eq(index).css("color","#246DFF");
	$(".type_select").eq(index).css("border-bottom","5px solid #246DFF");
	isClick[i] = true;
});