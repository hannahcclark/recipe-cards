$("document").ready(function () {
		$("#login").submit(function(event){
			event.preventDefault();
			$.ajax({
				url:"http://localhost:5000/login/", 
				type: "POST",
				data: $("form").serialize())
				success: function(data, textStatus, jqXHR) {},
    			error: function (jqXHR, textStatus, errorThrown){}
		});

});