 $(document).ready(function(){
	var listlength = $("ol#preparation li").length;
	$(".panel-heading").click(function(){
		$(".panel-body").toggle();
	});
	$(".modal-wide").on("show.bs.modal", function() {
		var counter = 0;
		var height = $(window).height() - 0;
		$(this).find(".modal-body").css("max-height", height);
		var sc = counter.toString();
		var stepinc = counter+1;
		$("div.modal-title").html("Step " + stepinc);
		$("div#ingreds").html($("ul#ingredients").html());
		$("div#instructs").html("<p>" + $("ol#preparation li").eq(counter).text() + "</p>");
		$("#nextbutton").click(function(){
			if (stepinc < listlength){
					counter++;
					stepinc++;
					$("div.modal-title").html("Step " + stepinc);
					$("div#instructs").html("<p>" + $("ol#preparation li").eq(counter).text() + "</p>");
				}
		});
		$("#backbutton").click(function(){
			if (stepinc > 1){
					counter--;
					stepinc--;
					$("div.modal-title").html("Step " + stepinc);
					$("div#instructs").html("<p>" + $("ol#preparation li").eq(counter).text() + "</p>");
				}
		});
		$("#toggleingredients").click(function(){
			$("#ingreds").toggle();
		});
		$(document).keydown(function(e){
			if (e.which == 75 || e.which==59 || e.which== 22 || e.which==47 
				|| e.which == 46 || e.which == 74 || e.which == 39 || e.which == 92
				|| e.which == 39 || e.which == 40 || e.which == 44 || e.which == 222
				|| e.which == 77 || e.which == 78 || e.which == 76 || e.which == 73 
				|| e.which == 85 || e.which == 79 || e.which == 80 || e.which == 91
				|| e.which == 93 || e.which == 10 || e.which == 16
				){
				
				if (stepinc < listlength){
					counter++;
					stepinc++;
					$("div.modal-title").html("Step " + stepinc);
					$("div#instructs").html("<p>" + $("ol#preparation li").eq(counter).text() + "</p>");
				}	
			} 
			else if (e.which == 32) {
				$("#ingreds").toggle();
			}
			else {
				if (stepinc > 1){
					counter--;
					stepinc--;
					$("div.modal-title").html("Step " + stepinc);
					$("div#instructs").html("<p>" + $("ol#preparation li").eq(counter).text() + "</p>");
				}
			}
	 	});
	});

 	$('#inclM').change(function() {
 		$("#locForm").toggle();
	});

 	$("#sms").click(function(){
 		$("#wrong-phone").hide();
 		if (!($("#phone").val() === "")) {
	 		if ($("#inclM").is(":checked")) {
	 			if($("#locForm input[type='radio']:checked").val() === "geoloc") {
	 				if (navigator.geolocation) {
						navigator.geolocation.getCurrentPosition(function(position) {
							getAddress(position.coords.latitude, position.coords.longitude,
								function(add) {
	 									sendSMS(stringifyIngredientList() + '\nMarket:\n' + add);
	 								});
						});
					}
	 				else {
	 					$("#wrong-phone").show();
	 				}
	 			}
	 			else {
	 				$.ajax('https://maps.googleapis.com/maps/api/geocode/json?address=' 
	 						+ $("#address").val(),//urlencode
	 				{
	 					dataType:'json',
	 					success: function(data) {
	 						if (data.status === "OK") {
	 							getAddress(data.results[0].geometry.location.lat, data.results[0].geometry.location.lng,
	 								function(add) {
	 									sendSMS(stringifyIngredientList() + '\nMarket:\n' + add);
	 								});
					 		}
					 		else {
					 			$("#wrong-phone").show();
					 		}
	 					},
	 					error: function() {$("#wrong-phone").show();}
	 				}
	 				);
	 			}
	 		}
	 		else {
	 			sendSMS(stringifyIngredientList());
	 		}
	 	}
	 	else {
	 		$("#wrong-phone").show();
	 	}
 	});
});
function stringifyIngredientList() {
	var ret = "\n";
	for (var i = 0; i < $("ul#ingredients li").length; i++) {
		ret = ret + $("ul#ingredients li").eq(i).text() + "\n";
	}
	return ret;
}

function getAddress(lat, lng, callback) {
	var service = new google.maps.places.PlacesService(document.getElementById('map'));
	var request = {
		location: new google.maps.LatLng(lat, lng),
		types: ["grocery_or_supermarket"],
		rankBy: google.maps.places.RankBy.DISTANCE
	};
	service.nearbySearch(request, function(results, status){
		if (status == google.maps.places.PlacesServiceStatus.OK) {
			var id = results[0].place_id;//Need additional step because not text search
			service.getDetails({placeId:id}, function(place, status){
				if (status == google.maps.places.PlacesServiceStatus.OK) {
					$("#map").html(place.html_attributions);
					callback(place.name + "\n" + place.formatted_address);
				}
				else {
					$("#wrong-phone").show();
				}
			});
		}
		else {
			$("#wrong-phone").show();
		}
	});
}

function sendSMS(text) {
	var phone = $("#phone").val();
	$.post("/sendSMS/", {'msg':text, 'phone':phone},
		function(data){$("#wrong-phone").hide();});
}