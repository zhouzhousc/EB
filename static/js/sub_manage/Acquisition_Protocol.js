//$(document).ready(function(){


function click_config(id){
	window.document.getElementById("acq_application_span").innerHTML = "自定义：";
	if(id == "modbus_rtu"){
		window.document.getElementById("tittle_span").innerHTML = "Modbus-RTU";
//		$(window.parent.document).find("#acq_save").attr("onclick","pop_acq_save('config_center_modbus')");
//		$(window.parent.document).find("#acq_close").attr("onclick","pop_acq_close('config_center_modbus')");
	}else if(id == "mqtt"){
		window.document.getElementById("tittle_span").innerHTML = "MQTT 协议";
//		$(window.parent.document).find("#acq_save").attr("onclick","pop_acq_save('config_center_mqtt')");
//		$(window.parent.document).find("#acq_close").attr("onclick","pop_acq_close('config_center_mqtt')");
	}
//	else if(id == "application"){
//		parent.window.document.getElementById("acq_application_span").innerHTML = "应用";
//		parent.window.document.getElementById("tittle_span").innerHTML = "";
//	}
	window.document.getElementById("acq_application").style.display = "none";
	window.document.getElementById("modbus_rtu").style.display = "none";
//	parent.window.document.getElementById("config_center_mqtt").style.display = "none";
	window.document.getElementById("podiv").style.display = "block";
	window.document.getElementById("config_podiv").style.display = "block";
	window.document.getElementById(id).style.display = "block";
}

function click_application(etr_name){
	window.document.getElementById("acq_save").setAttribute("etr_name",etr_name);
	window.document.getElementById("modbus_rtu").style.display = "none";
	window.document.getElementById("acq_application_span").innerHTML = "应用";
	window.document.getElementById("tittle_span").innerHTML = "";
	window.document.getElementById("acq_application").style.display = "block";
	window.document.getElementById("podiv").style.display = "block";
//	parent.window.document.getElementById("config_podiv").style.display = "block";
}

function pop_close(id){
	window.document.getElementById(id).style.display = "none";
	// window.document.getElementById("acq_bottom_tips").style.display = "block";
	window.document.getElementById("acq_application").style.display = "none";
	window.document.getElementById("podiv").style.display = "none";
	// window.document.getElementById("podiv").style.display = "none";
	// window.document.getElementById("modbus_rtu").style.display = "block";
}

var list = ["config_center_modbus"];

$(function(){
        $('table tr').each(function(){
            $(this).find('.acq_details').click(function(){
//          	$(this).children("img").src="../../img/sub_manage/u1722.png";
//             	$("table img").attr("src","../../img/sub_manage/u1719.png");
            	$("tr").css("background-color","");
            	if($(this).parents('tr').next('.box').is(":visible")){
					// $(this).children("img").attr("src","../../img/sub_manage/u1719.png");
					$(this).parents('tr').css("background-color","");
					$(this).parents('tr').next('.box').hide();
				}else{
            		$(".box").hide();
					// $(this).children("img").attr("src","../../img/sub_manage/u1722.png");
					$(this).parents('tr').css("background-color","#d5eaff");
					$(this).parents('tr').next('.box').show();
				}
            });
        });
//      $(document).click(function(e){z
//          var target = $(e.target);
//          if(target.closest("table tr").length == 0){
//              $(".box").hide();
//          }
//      });
		$("#acq_submit").click(function (){
			var value;
			var select_box = $("#select_box input").val();

		   	if(select_box == "RS232接口类"){
		   		value = $("#rs232 input").val();
		   	}else if(select_box == "以太网类型"){
		   		value = $("#intel input").val();
		   	}else if(select_box == "专有类型"){
		   		value = $("#other input").val();
		   	}
			if(value == "请选择协议名称"){
				$("#tips_select").css("display","block");
				$("#tips_select").stop(true,false).animate({
			  	  opacity: 1
				}, 1000,function (){
					$("#tips_select").animate({
			        	opacity: 0
			   		}, 3000,function (){
						$("#tips_select").css("display","none");
			   		 });
				});
			}else if(value == "ModBus-RTU"){
				click_config('modbus_rtu');
//				$("#acq_submit").attr("onclick","click_config('config_center_modbus')");
//				$("#acq_submit").click();
			}else if(value == "MQTT"){
				click_config('mqtt');
			}
		})
    })

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
	   	var value = $(this).text();
	   	if(value == "RS232接口类"){
			$(".myselect").css("color","");
			$(".myselect").val("请选择协议名称");
	   		$("#rs232").css("display","block");
	   		$("#intel").css("display","none");
	   		$("#other").css("display","none");
	   	}else if(value == "以太网类型"){
			$(".myselect").css("color","");
			$(".myselect").val("请选择协议名称");
	   		$("#rs232").css("display","none");
	   		$("#intel").css("display","block");
	   		$("#other").css("display","none");
	   	}else if(value == "专有类型"){
			$(".myselect").css("color","");
			$(".myselect").val("请选择协议名称");
	   		$("#rs232").css("display","none");
	   		$("#intel").css("display","none");
	   		$("#other").css("display","block");
	   	}else{
			$(".myselect").css("color","#333333");
	   	}

   }).hover(function(){$(this).addClass("hover");},function(){$(this).removeClass("hover");});
  }else{
   thisul.fadeOut("fast");
  }
 });

$("#hide_div").hide();
$("#acq_modbus").hover(function () {
    	$("#hide_div").show();
	}, function () {
        $("#hide_div").hide();
	});
// 鼠标移动到list的div上的时候list div不会被隐藏
$("#hide_div").hover(function () {
    	$("#hide_div").show();
    }, function () {
        $("#hide_div").hide();
	});
//});