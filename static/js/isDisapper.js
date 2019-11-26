if($("#copy_success", window.parent.document).css("opacity") == 0){
}else{
	var opa = $("#copy_success", window.parent.document).css("opacity");
	if(opa >= 0.5){
//		console.log("opa大于0.5：");
//		console.log(opa);
		$("#copy_success", window.parent.document).animate({
			opacity: 0
		}, 2000,function(){
		    $("podiv_tips", window.parent.document).css("display","none");
		    $("copy_success", window.parent.document).css("display","none");
		});
		$("#copy_error", window.parent.document).animate({
			opacity: 0
		}, 2000,function(){
		    $("podiv_tips", window.parent.document).css("display","none");
		    $("copy_error", window.parent.document).css("display","none");
		});
	}
	if(opa <= 0.5){
//		console.log("opa小于0.5：");
//		console.log(opa);
		$("#copy_success", window.parent.document).animate({
			opacity: 0
		}, 1000,function(){
		    $("podiv_tips", window.parent.document).css("display","none");
		    $("copy_success", window.parent.document).css("display","none");
		});
		$("#copy_error", window.parent.document).animate({
			opacity: 0
		}, 1000,function(){
		    $("podiv_tips", window.parent.document).css("display","none");
		    $("copy_error", window.parent.document).css("display","none");
		});
	}
}
