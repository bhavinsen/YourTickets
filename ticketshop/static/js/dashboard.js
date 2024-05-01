$(document).bind("ajaxSend", function() {
  $(".dashboard-loading").show();
}).bind("ajaxComplete", function() {
  $(".dashboard-loading").hide();
});
document.addEventListener("DOMContentLoaded", function(event) {
  urlPage();
});
window.onhashchange = function() {
	urlPage();
}
function urlPage() {
    var page = window.location.hash.substr(1);
	if (page > 1 && page < 4 ) {
	  $('#js-dashboard-container').load('dashboard-'+ page +'.html');
	  $("[id^=js-page-]").removeClass("dashboard-active");
	  $("#js-page-"+ page).addClass("dashboard-active");
	}
	else{
		$('#js-dashboard-container').load('dashboard-1.html');
		$("[id^=js-page-]").removeClass("dashboard-active");
	    $("#js-page-1").addClass("dashboard-active");
	}
}
