var boo = false;
$(function () {
    $('.click_copy').each(function (num) {
        var clipboard = new ClipboardJS(this, {
            target: function () {
                return document.querySelectorAll('.topic')[num];
            }
        });
           
        var tips = parent.window.document.getElementById("podiv_tips");
        var succ = parent.window.document.getElementById("copy_success");
        var erro = parent.window.document.getElementById("copy_error");
        
        if(boo == true){
        	setTimeout(function(){
        		clipboard.on('success', function (e) {
		        	tips.style.display = "block";
					succ.style.display = "block";
		            $(succ).animate({
				        opacity: 1
				    }, 1000,function(){
				    	boo = true;
					    if(boo == true){
					   		$(succ).animate({
						        opacity: 0
						    }, 2000,function(){
					    	console.log("bb");
					        	tips.style.display = "none";
								succ.style.display = "none";
								boo = false;
						    });
				    	}
				    });
		        });
		        clipboard.on('error', function (e) {
		        	tips.style.display = "block";
					erro.style.display = "block";
		            $("#copy_error").animate({
				        opacity: 1
				    }, 1000,function(){
				    	boo = true;
					    $("#copy_error").animate({
					        opacity: 0
					    }, 2000,function(){
				        	tips.style.display = "none";
							erro.style.display = "none";
							boo = false;
					    });
				    });
		        });
        	}, 5000);
        }else{
        	clipboard.on('success', function (e) {
	        	tips.style.display = "block";
				succ.style.display = "block";
	            $(succ).animate({
			        opacity: 1
			    }, 1000,function(){
			    	boo = true;
			    	if(boo == true){
				   		$(succ).animate({
					        opacity: 0
					    }, 2000,function(){
				    	console.log("bb");
				        	tips.style.display = "none";
							succ.style.display = "none";
							boo = false;
					    });
			    	}
			    });
	        });
	        clipboard.on('error', function (e) {
	        	tips.style.display = "block";
				erro.style.display = "block";
	            $("#copy_error").animate({
			        opacity: 1
			    }, 1000,function(){
			    	boo = true;
				    $("#copy_error").animate({
				        opacity: 0
				    }, 2000,function(){
			        	tips.style.display = "none";
						erro.style.display = "none";
						boo = false;
				    });
			    });
	        });
        }
        
        
    });
});