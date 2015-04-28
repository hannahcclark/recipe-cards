$(document).ready(function(){
	$(".modal-wide").on("show.bs.modal", function() {
		var counter = 0;
		var height = $(window).height() - 200;
		$(this).find(".modal-body").css("max-height", height);
		var sc = counter.toString();
		var stepinc = counter + 1;
		$("div.modal-title").html("Step " + stepinc);
		$("div.modal-body").html("<p>" + $("ol li").eq(counter).text() + "</p>");
		$(document).keypress(function(e){
			counter = (counter + 1) % $("ol li").length;
			stepinc = counter + 1;
			$("div.modal-title").html("Step " + stepinc);
			$("div.modal-body").html("<p>" + $("ol li").eq(counter).text() + "</p>");
 		});
	});
});