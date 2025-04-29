$(document).ready(function () {

    $('.copy-btn').click(function(e){
        var copy_inf = $(this).parent().find("span");
        var $temp = $("<input>");
        $("body").append($temp);
        $temp.val(copy_inf.text()).select();
	    document.execCommand("copy");
	    $temp.remove();
        copy_inf.addClass("select-active");
        setTimeout(function() {
            copy_inf.removeClass("select-active");
        }, 300);
    });

});