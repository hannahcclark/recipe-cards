 $(document).ready(function(){
	
	$(".modal-wide").on("show.bs.modal", function() {
		var counter = 1;
	var height = $(window).height() - 200;
	$(this).find(".modal-body").css("max-height", height);
	var sc = counter.toString();
	var stepnum = "step " + "fdsnklfds" +counter;
	$("div.modal-title").html(stepnum);
	$(document).keypress(function(e){
		 counter++;

		 $("div.modal-title").html("strep " + counter);
	$("div.modal-body").html("<p>hey " + counter +"</p>");
 });
});


 });