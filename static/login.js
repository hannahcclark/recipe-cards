$("document").ready(function () {
		$("#login").submit(function(event){
			var user = $("login-email").val();
			var pass = $("login-password").val();
			//entrypts user/password

			$.post("url", function(data){
				
			});
		});

});