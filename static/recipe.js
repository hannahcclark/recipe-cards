 $(document).ready(function(){
	var listlength = $("ol#preparation li").length;
	$(".modal-wide").on("show.bs.modal", function() {
	
	var counter = 0;
	var height = $(window).height() - 200;
	$(this).find(".modal-body").css("max-height", height);
	var sc = counter.toString();
	var stepinc = counter+1;
	$("div.modal-title").html("Step " + stepinc);
	$("div.modal-body").html("<p>" + $("ol li").eq(counter).text() + "</p>");
	$(document).keydown(function(e){
		console.log(e.which);
		if (e.which == 75 || e.which==59 || e.which== 22 || e.which==47 
			|| e.which == 46 || e.which == 74 || e.which == 39 || e.which == 92
			|| e.which == 39 || e.which == 40 || e.which == 44 || e.which == 222
			|| e.which == 77 || e.which == 78 || e.which == 76 || e.which == 73 
			|| e.which == 85 || e.which == 79 || e.which == 80 || e.which == 91
			|| e.which == 93 || e.which == 10 || e.which == 16 || e.which == 32
			){
			
			if (stepinc < listlength){
				counter = (counter + 1) % $("ol li").length;
				stepinc++;
				$("div.modal-title").html("Step " + stepinc);
				$("div.modal-body").html("<p>" + $("ol li").eq(counter).text() + "</p>");
			}	
		} 
		else {
			if (stepinc > 1){
				counter = (counter -1) % $("ol li").length;
				stepinc--;
				$("div.modal-title").html("Step " + stepinc);
				$("div.modal-body").html("<p>" + $("ol li").eq(counter).text() + "</p>");
			}
		}
 		});
	});
});