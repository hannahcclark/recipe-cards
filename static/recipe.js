var i = 0;
$(document).ready(function(){
$(".modal-wide").on("show.bs.modal", function() {
  var height = $(window).height() - 200;
  var modal = $(this).find(".modal-body");
  var body = $('ul li').toArray()[i].text();
  modal.css("max-height", height);
  modal.html("<p>" + i + ". " + body + "</p>");
  i++;
});
});