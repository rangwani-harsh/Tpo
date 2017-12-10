//progree bar
$(document).ajaxStart(function() {
// show loader on start
$("progress").css("display","block");
}).ajaxSuccess(function() {
// hide loader on success
$("progress").css("display","none");
});

//tool-tip init
$(document).ready(function(){
	$('[data-toggle="tooltip"]').tooltip();
});